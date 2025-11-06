# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Apple-Inspired Streamlit App", page_icon="🍎", layout="wide")
st.title("")  # prevent Streamlit from injecting extra header space

# Read query param for simple routing
params = st.experimental_get_query_params()
page = params.get("page", ["0"])[0]

# The HTML/CSS/JS chunk (Tailwind via CDN + Lucide icons)
# We'll render this entire block via st.components.v1.html so HTML is not escaped.
base_html = """
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://unpkg.com/lucide-static@latest/font/lucide.css" rel="stylesheet">

<style>
  :root { --bg-light: linear-gradient(to bottom right,#f9fafb,#ffffff); --bg-dark: linear-gradient(to bottom right,#0b1220,#111827); }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin:0; padding:0; }
  [data-theme='light'] { background: var(--bg-light); color: #0f172a; }
  [data-theme='dark'] { background: var(--bg-dark); color: #e6eef8; }

  .app-shell { padding: 20px 32px; min-height: 380px; box-sizing: border-box; }
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
  // Theme persistence
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('theme', theme); } catch(e){}
  }
  function toggleTheme() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(cur === 'dark' ? 'light' : 'dark');
  }
  document.addEventListener('DOMContentLoaded', function() {
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
  });
</script>
"""

# Helpers to produce page-specific HTML
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
    return f"""
    <div class="page-wrap fade">
      <div class="page-title">{title}</div>
      <div class="page-desc">{desc}</div>
      <a class="link" href="?page=0">← Back to Home</a>
    </div>
    """

# Build the final HTML to inject into Streamlit component
html_parts = [base_html, '<div class="app-shell">', render_nav()]

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
    html_parts.append(render_page("Page not found", "The page parameter is invalid — returning to Home."))

html_parts.append('</div>')  # close app-shell
final_html = "\n".join(html_parts)

# Render via components.html so HTML is not escaped
# Height is set to 800 to comfortably show content; Streamlit will allow scrolling.
components.html(final_html, height=800, scrolling=True)
