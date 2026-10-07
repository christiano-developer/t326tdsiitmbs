// Page enhancements for the docs site. Runs on every page, including instant-navigation loads
// (Material's document$ observable fires after each page swap).
document$.subscribe(() => {
  collapseTables();
  headerPager();
});

// Wrap every content table in a collapsed <details>; opening one closes the others (accordion).
function collapseTables() {
  const tables = document.querySelectorAll(".md-content article table:not(.np-done)");
  tables.forEach((table) => {
    table.classList.add("np-done");
    // Material wraps tables in .md-typeset__scrollwrap; move that wrapper if present
    const block = table.closest(".md-typeset__scrollwrap") || table;
    const details = document.createElement("details");
    details.className = "np-table";
    details.name = "np-tables"; // native exclusive accordion in current browsers

    const summary = document.createElement("summary");
    // Label with the column names (the heading above already names the table)
    const rows = table.tBodies[0] ? table.tBodies[0].rows.length : 0;
    const cols = [...table.querySelectorAll("thead th")].map((th) => th.textContent.trim()).filter(Boolean);
    summary.textContent = cols.join(" · ") || "Table";
    const meta = document.createElement("span");
    meta.className = "np-meta";
    meta.textContent = `${rows} ${rows === 1 ? "row" : "rows"}`;
    summary.append(meta);

    block.before(details);
    details.append(summary, block);
  });

  // Fallback for browsers without <details name>: close siblings on open
  document.querySelectorAll("details.np-table").forEach((d) => {
    if (d.dataset.npBound) return;
    d.dataset.npBound = "1";
    d.addEventListener("toggle", () => {
      if (!d.open) return;
      document.querySelectorAll("details.np-table[open]").forEach((o) => o !== d && (o.open = false));
    });
  });
}

// Copy the footer's previous/next links into the header so they are always visible
function headerPager() {
  const inner = document.querySelector(".md-header__inner");
  if (!inner) return;
  inner.querySelector(".np-pager")?.remove();

  const pager = document.createElement("nav");
  pager.className = "np-pager";
  pager.setAttribute("aria-label", "Previous and next page");
  pager.append(pagerLink(".md-footer__link--prev", "←", "Previous", true),
               pagerLink(".md-footer__link--next", "→", "Next", false));
  const search = inner.querySelector(".md-search") || inner.querySelector(".md-header__source");
  search ? search.before(pager) : inner.append(pager);
}

function pagerLink(selector, arrow, fallback, arrowFirst) {
  const src = document.querySelector(selector);
  const a = document.createElement("a");
  const label = document.createElement("span");
  label.textContent = src?.querySelector(".md-ellipsis")?.textContent.trim() || fallback;
  a.title = `${fallback}: ${label.textContent}`;
  if (src) a.href = src.href;
  else a.setAttribute("aria-disabled", "true");
  arrowFirst ? a.append(arrow, label) : a.append(label, arrow);
  return a;
}
