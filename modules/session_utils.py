import uuid


def get_or_create_user_id(existing: str | None) -> str:
    """Return existing user id or create a new one."""
    if existing:
        return existing
    return str(uuid.uuid4())

