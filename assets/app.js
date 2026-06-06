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

// Initial setup listener
document.addEventListener("DOMContentLoaded", () => {
  console.log("[Nexora AI] UI script loaded successfully.");
});
