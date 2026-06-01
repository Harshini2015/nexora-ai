import os
import time
import json
from typing import Any

import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()

_model = None


def init_gemini():
    global _model
    if _model is not None:
        return _model

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)
    _model = genai.GenerativeModel("gemini-pro")
    return _model


def _extract_json_object(text: str) -> str:
    """Best-effort extraction of the first JSON object from model output."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found")
    return text[start : end + 1]


def _validate_types(payload: Any, schema: dict[str, Any]) -> None:
    """Very small validator for required keys and basic types."""
    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")

    for key, expected in schema.items():
        if key not in payload:
            raise ValueError(f"Missing key: {key}")

        val = payload[key]
        if expected is int:
            if not isinstance(val, int):
                raise ValueError(f"{key} must be int")
        elif expected is str:
            if not isinstance(val, str):
                raise ValueError(f"{key} must be str")
        elif expected is list:
            if not isinstance(val, list):
                raise ValueError(f"{key} must be list")
        else:
            # schema can be nested (not used currently)
            pass


def get_gemini_response(prompt, history=None, retries=3, delay=2):
    for i in range(retries):
        try:
            model = init_gemini()
            if history:
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
            else:
                response = model.generate_content(prompt)

            if not response or not getattr(response, "text", None):
                return "Error: Gemini returned an empty response."
            return response.text

        except exceptions.ResourceExhausted:
            if i < retries - 1:
                time.sleep(delay * (2**i))
                continue
            return "Error: Gemini API rate limit exceeded. Please try again later."
        except exceptions.ServiceUnavailable:
            if i < retries - 1:
                time.sleep(delay * (2**i))
                continue
            return "Error: Gemini service is currently unavailable. Please try again later."
        except Exception as e:
            return f"Error: {str(e)}"
    return "Error: Maximum retries reached."


def get_gemini_json(prompt: str, schema: dict[str, Any], retries: int = 3, delay: int = 2) -> dict[str, Any]:
    """Call Gemini and force JSON parsing/validation.

    Returns a dict on success.
    Raises ValueError after exhausting retries.
    """
    last_err: Exception | None = None

    for i in range(retries):
        try:
            raw = get_gemini_response(
                prompt,
                history=None,
                retries=1,
                delay=delay,
            )

            if isinstance(raw, str) and raw.startswith("Error:"):
                raise ValueError(raw)

            if not isinstance(raw, str):
                raise ValueError("Gemini output is not text")

            json_str = _extract_json_object(raw)
            payload = json.loads(json_str)
            _validate_types(payload, schema)
            return payload

        except Exception as e:
            last_err = e
            if i < retries - 1:
                time.sleep(delay * (2**i))
                continue

    raise ValueError(f"Invalid JSON from Gemini after {retries} attempts: {last_err}")

