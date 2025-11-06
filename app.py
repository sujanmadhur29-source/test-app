# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Apple-Inspired Streamlit App", page_icon="🍎", layout="wide")
# avoid Streamlit default header spacing
st.title("")

# read query param for routing
params = st.experimental_get_query_params()
page = params.get("page", ["0"])[0]

# ------------------------------------------------------------------
# HTML/CSS/JS to inject. This block includes:
# - styles
# - theme toggle (localStorage)
# - auto-resize script that posts height to parent
# - fallback internal scrolling if parent doesn't accept resize
# ------------------------------------------------------------------
base_html = r"""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://unpkg.com/lucide-static@latest/font/lucide.css" rel="stylesheet">

<style>
  :root { --bg-light: linear-gradient(to bottom right,#f9fafb,#ffffff); --bg-dark: linear-gradient(to bottom right,#0b1220,#111827); }
  html,body { height: 100%; margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  [data-theme='light'] { background: var(--bg-light); color: #0f172a; }
  [data-theme='dark'] { background: var(--bg-dark); color: #e6eef8; }

  /* outer wrapper that we ask Streamlit to size to content */
  .app-shell { box-sizing: border-box; padding: 20px 32px; width: 100%; display: block; }

  /* If parent doesn't allow dynamic resize, .inner-scroll will handle internal scroll */
  .inner-scroll { max-height: 100vh; overflow: auto; padding-bottom: 28px; box-sizing: border-box; }

  .nav { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:18px; }
  .brand { display:flex; align-items:center; gap:10px; font-weight:600; font-size:18px; }
  .nav-buttons { display:flex; gap:8px; align-items:center; }
  .nav-button { background: rgba(255,255,255,0.75); border-radius:12px; padding:8px 12px; cursor:pointer; border:0; font-weight:500; transition: transform 180ms ease, background 180ms ease; }
  [data-theme='dark'] .nav-button { background: rgba(255,255,255,0.06); color: #e6eef8; }
  .nav-button:hover { transform: translateY(-3px); }

  .toggle-btn { cursor:pointer; padding:6px; border-radius:10px; }

  .grid { display:grid; grid-template-columns: repeat(1, minmax(0,1fr)); gap:18px; }
  @media(min-width:768px){ .grid { grid-template-columns: repeat(3, minmax(0,1fr)); } }

  .apple-card {
    background: rgba(255,255,255,0.85);
    border-radius:16px;
    padding:22px;
    box-shadow: 0 10px 30px rgba(2,6,23,0.06);
    transition: transform .25s ease, box-shadow .25s ease;
    min-height:120px;
  }
  [data-theme='dark'] .apple-card {
    background: rgba(17,24,39,0.85);
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
  }
  .apple-card:hover { transform: translateY(-6px); box-shadow: 0 18px 50px rgba(2,6,23,0.12); }

  .card-title { font-size:18px; font-weight:600; margin-bottom:8px; }
  .card-body { color: #6b7280; }
  [data-theme='dark'] .card-body { color: #9ca3af; }
  .link { display:inline-block; margin-top:10px; color:#0066ff; font-weight:600; text-decoration:none; }
  [data-theme='dark'] .link { color:#66a3ff; }

  .page-wrap { margin-top:10px; padding:18px; border-radius:12px; background:transparent; }
  .page-title { font-size:28px; font-weight:700; margin-bottom:8px; }
  .page-desc { color:#6b7280; margin-bottom:12px; }
  [data-theme='dark'] .page-desc { color:#cbd5e1; }

  .center { text-align:center; }
  .fade { animation: fadeIn .45s ease both; }
  @keyframes fadeIn { from { opacity:0; transform: translateY(8px);} to { opacity:1; transform: translateY(0);} }
</style>

<script>
  // Theme persistence logic
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('theme', theme); } catch (e) {}
  }
  function toggleTheme() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(cur === 'dark' ? 'light' : 'dark');
    // After toggling theme, recompute and send new height
    setTimeout(postHeightToParent, 120);
  }
  document.addEventListener('DOMContentLoaded', function() {
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
    // Initial post of height after DOM loaded
    setTimeout(postHeightToParent, 120);
  });

  // Auto-resize: compute document height and post message to parent to request frame height update.
  function getDocHeight() {
    const body = document.body;
    const html = document.documentElement;
    return Math.max(
      body.scrollHeight, body.offsetHeight,
      html.clientHeight, html.scrollHeight, html.offsetHeight
    );
  }

  function postHeightToParent() {
    const h = getDocHeight();
    // Streamlit listens to a special message type for resizing: setFrameHeight
    // We attempt both known patterns for compatibility.
    try {
      // Preferred: Streamlit's internal receiver
      window.parent.postMessage({isStreamlitMessage: true, type: 'setFrameHeight', height: h}, '*');
    } catch (e) {
      // fallback general message
      window.parent.postMessage({type: 'setFrameHeight', height: h}, '*');
    }
  }

  // Observe DOM changes and post updated height (handles navigation content changes)
  const observer = new MutationObserver(function() {
    postHeightToParent();
  });
  observer.observe(document.documentElement || document.body, { childList: true, subtree: true, characterData: true });

  // Also post height on window resize (responsive)
  window.addEventListener('resize', function() {
    setTimeout(postHeightToParent, 80);
  });
</script>
"""

# Helper functions to build inner HTML blocks
def render_nav():
    return """
    <div class="nav">
      <div class="brand"><i class="lucide lucide-apple" style="font-size:20px;"></i><span>Streamlit OS</span></div>
      <div class="nav-buttons">
        <button class="nav-button" onclick="window.location.href='?page=0'"><i class="lucide lucide-home"></i>&nbsp;Home</button>
        <button class="nav-button" onclick="window.location.href='?page=1'"><i class="lucide lucide-monitor"></i>&nbsp;Page 1</button>
        <button class="nav-button" onclick="window.location.href='?page=2'"><i class="lucide lucide-bar-chart"></i>&nbsp;Page 2</button>
        <button class="nav-button" onclick="window.location.href='?page=3'"><i class="lucide lucide-file-text"></i>&nbsp;Page 3</button>
        <button class="nav-button" onclick="window.location.href='?page=4'"><i class="lucide lucide-users"></i>&nbsp;Page 4</button>
        <button class="nav-button" onclick="window.location.href='?page=5'"><i class="lucide lucide-settings"></i>&nbsp;Page 5</button>
      </div>
      <div class="toggle-btn" title="Toggle theme" onclick="toggleTheme()">
        <i class="lucide lucide-sun" style="font-size:18px;"></i>
      </div>
    </div>
    """

def render_home_cards():
    return """
    <div class="grid">
      <div class="apple-card fade">
        <div class="card-title">Page 1 — Overview</div>
        <div class="card-body">Intro, value proposition and product highlights.</div>
        <a class="link" href="?page=1">Open →</a>
      </div>

      <div class="apple-card fade">
        <div class="card-title">Page 2 — Analytics</div>
        <div class="card-body">Dashboards, charts and KPIs.</div>
        <a class="link" href="?page=2">Open →</a>
      </div>

      <div class="apple-card fade">
        <div class="card-title">Page 3 — Reports</div>
        <div class="card-body">Exportable reports & tables.</div>
        <a class="link" href="?page=3">Open →</a>
      </div>

      <div class="apple-card fade">
        <div class="card-title">Page 4 — Collaboration</div>
        <div class="card-body">Team boards, comments and shared views.</div>
        <a class="link" href="?page=4">Open →</a>
      </div>

      <div class="apple-card fade">
        <div class="card-title">Page 5 — Settings</div>
        <div class="card-body">Profile, preferences and integrations.</div>
        <a class="link" href="?page=5">Open →</a>
      </div>
    </div>
    """

def render_page(title, desc):
    # note: Back link updates query param and causes Streamlit rerun
    return f"""
    <div class="page-wrap fade">
      <div class="page-title">{title}</div>
      <div class="page-desc">{desc}</div>
      <a class="link" href="?page=0">← Back to Home</a>
    </div>
    """

# Build final HTML:
# We place content inside .inner-scroll so that if the host refuses dynamic resizing,
# the inner area will scroll without causing Streamlit layout jumps.
html_parts = [
    base_html,
    '<div class="app-shell">',
    '<div class="inner-scroll">',  # inner scroll container (fallback)
    render_nav()
]

if page == "0":
    html_parts.append('<div class="center"><h1 style="font-size:36px;margin-bottom:6px;">🍎 Welcome to Streamlit OS</h1>')
    html_parts.append('<p style="color:#6b7280;margin-bottom:16px;">Apple-inspired multipage UI — Tailwind + Lucide icons.</p></div>')
    html_parts.append(render_home_cards())
elif page == "1":
    html_parts.append(render_page("Page 1 — Overview", "Overview, features and product description."))
elif page == "2":
    html_parts.append(render_page("Page 2 — Analytics", "Interactive charts (you can embed Altair/Plotly here)."))
elif page == "3":
    html_parts.append(render_page("Page 3 — Reports", "Downloadable reports and export options."))
elif page == "4":
    html_parts.append(render_page("Page 4 — Collaboration", "Team tools, shared spaces and comments."))
elif page == "5":
    html_parts.append(render_page("Page 5 — Settings", "Preferences, theming and account settings."))
else:
    html_parts.append(render_page("Page not found", "Invalid page parameter — returning to Home."))

html_parts.append('</div>')  # close inner-scroll
html_parts.append('</div>')  # close app-shell
final_html = "\n".join(html_parts)

# Render with components.html
# Height: we set a reasonably large default height; the embedded script will attempt to resize it to exact content height.
# If resizing is not accepted by the host, the inner-scroll area will provide internal scrolling and stop Streamlit layout jumps.
components.html(final_html, height=900, scrolling=True)
