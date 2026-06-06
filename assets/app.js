/**
 * Nexora AI Client-Side Scripts
 */

// Toggle sidebar collapse
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  if (sidebar) {
    sidebar.classList.toggle("collapsed");
    console.log("[Nexora AI] Sidebar toggle status:", sidebar.classList.contains("collapsed"));
  }
}

// Make toggle accessible globally in browser
window.toggleSidebar = toggleSidebar;

// Navigate to selected page on client side
function navigateToPage(pageName) {
  const pages = ["home", "chat", "resume", "interview", "career", "settings"];
  pages.forEach(p => {
    // Show/hide page columns
    const pageEl = document.getElementById(`page-${p}`);
    if (pageEl) {
      if (p === pageName) {
        pageEl.style.setProperty("display", "flex", "important");
      } else {
        pageEl.style.setProperty("display", "none", "important");
      }
    }
    // Update active button state
    const btnEl = document.getElementById(`nav-${p}`);
    if (btnEl) {
      if (p === pageName) {
        btnEl.classList.add("active");
      } else {
        btnEl.classList.remove("active");
      }
    }
  });
}
window.navigateToPage = navigateToPage;

// Initial setup listener
document.addEventListener("DOMContentLoaded", () => {
  console.log("[Nexora AI] UI script loaded successfully.");
});
