# app.py
import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Apple-Inspired Streamlit App", page_icon="🍎", layout="wide")

# --- Session defaults ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # 'light' or 'dark'

# Helper to navigate
def navigate(p):
    st.session_state.page = p

# --- Minimal CSS (Apple-ish) injected natively ---
# We keep CSS minimal and scoped to avoid interfering with Streamlit internals.
base_css = f"""
<style>
:root {{
  --bg-light: #f7f8fa;
  --bg-dark: #0f1724;
  --card-light: rgba(255,255,255,0.95);
  --card-dark: rgba(17,24,39,0.88);
  --muted-light: #6b7280;
  --muted-dark: #9ca3af;
  --accent: #0b69ff;
  --radius: 14px;
  --glass: rgba(255,255,255,0.6);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}

/* Theme */
[data-theme="light"] .stApp {{
  background: linear-gradient(180deg, var(--bg-light), #ffffff);
  color: #0f1724;
}}
[data-theme="dark"] .stApp {{
  background: linear-gradient(180deg, #041026, var(--bg-dark));
  color: #e6eef8;
}}

/* Top nav */
.app-header {{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding:18px 22px;
  border-radius: 12px;
  margin-bottom: 12px;
}}
.brand {{
  display:flex;
  align-items:center;
  gap:12px;
  font-size:20px;
  font-weight:700;
}}
.brand .logo {{
  display:inline-flex;
  width:40px;
  height:40px;
  border-radius:10px;
  align-items:center;
  justify-content:center;
  font-size:20px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.06);
}}

/* Nav buttons */
.nav-row {{
  display:flex;
  gap:8px;
  align-items:center;
}}
.nav-btn {{
  background:var(--card-light);
  border-radius: 10px;
  padding:8px 12px;
  font-weight:600;
  border: none;
  cursor: pointer;
  transition: transform .12s ease, box-shadow .12s ease;
}}
[data-theme="dark"] .nav-btn {{ background: var(--card-dark); }}
.nav-btn:hover {{ transform: translateY(-3px); box-shadow: 0 10px 30px rgba(2,6,23,0.08); }}

/* Page container: fixed min height reduces jumps when content changes */
.page-container {{
  min-height: 640px;     /* <-- important: prevents container jumps across pages */
  padding: 22px;
  border-radius: 12px;
  margin-bottom: 18px;
}}

/* Cards grid */
.cards {{
  display: grid;
  gap: 18px;
  grid-template-columns: 1fr;
}}
@media(min-width:900px) {{
  .cards {{ grid-template-columns: repeat(3, 1fr); }}
}}
.card {{
  background: var(--card-light);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: 0 10px 30px rgba(2,6,23,0.06);
  transition: transform .16s ease, box-shadow .16s ease;
  min-height: 120px;
}}
[data-theme="dark"] .card {{ background: var(--card-dark); box-shadow: 0 8px 24px rgba(0,0,0,0.6); }}
.card:hover {{ transform: translateY(-6px); box-shadow: 0 18px 52px rgba(2,6,23,0.12); }}
.card-title {{ font-size:18px; font-weight:700; margin-bottom:8px; }}
.card-desc {{ color: var(--muted-light); }}
[data-theme="dark"] .card-desc {{ color: var(--muted-dark); }}

/* small utility */
.kv-row {{ display:flex; align-items:center; gap:8px; margin-top:8px; }}
.btn-link {{
  color: var(--accent);
  font-weight:700;
  text-decoration: none;
}}
.small-muted {{ color: var(--muted-light); font-size:13px; }}
[data-theme="dark"] .small-muted {{ color: var(--muted-dark); }}

/* Sidebar tweaks */
[data-testid="stSidebar"] {{
  border-radius: 12px;
}}

/* make Streamlit's main container use our theme attribute */
</style>
"""

# Inject CSS and set theme attribute on document root via a tiny script
# Using st.markdown unsafe HTML to set data-theme on top-level element.
theme_script = f"""
<script>
const theme = "{st.session_state.theme}";
document.documentElement.setAttribute('data-theme', theme);
</script>
"""

# Render CSS + script
st.markdown(base_css + theme_script, unsafe_allow_html=True)

# --- Header with native Streamlit layout (columns) ---
with st.container():
    cols = st.columns([1, 3, 1])
    with cols[0]:
        # Brand area
        st.markdown(
            """
            <div class="app-header">
              <div class="brand">
                <div class="logo">🍎</div>
                <div>
                  <div style="font-weight:700;">Streamlit OS</div>
                  <div style="font-size:12px;color:gray;margin-top:2px;">Apple-inspired UI</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        # Centered nav buttons (native Streamlit buttons)
        nav_col1, nav_col2 = st.columns([1, 1])
        # We'll render as buttons using st.button so clicks are native and predictable.
        # Using forms would be overkill; st.button updates session_state on click.
        nav_buttons = st.container()
        # Create a row of buttons with consistent styles using HTML-wrapped buttons that trigger query param navigation.
        # But to keep everything native, use st.button in a single row via columns:
        bcols = st.columns([1,1,1,1,1,1])
        if bcols[0].button("Home"):
            navigate("home")
        if bcols[1].button("Page 1"):
            navigate("page1")
        if bcols[2].button("Page 2"):
            navigate("page2")
        if bcols[3].button("Page 3"):
            navigate("page3")
        if bcols[4].button("Page 4"):
            navigate("page4")
        if bcols[5].button("Page 5"):
            navigate("page5")
    with cols[2]:
        # Theme toggle (native)
        tcol1, tcol2 = st.columns([2,1])
        with tcol1:
            # small label to indicate theme mode
            if st.session_state.theme == "light":
                st.write("")  # spacing
            else:
                st.write("")
        with tcol2:
            # Theme switch: checkbox toggles theme
            new_theme = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
            # If toggle changed, update session_state and rerun to apply new CSS attribute
            if new_theme and st.session_state.theme != "dark":
                st.session_state.theme = "dark"
                st.experimental_rerun()
            if not new_theme and st.session_state.theme != "light":
                st.session_state.theme = "light"
                st.experimental_rerun()

# --- Page Rendering: native Streamlit controls only ---
# Wrap page content in a container with class `page-container` (applies min-height)
page_container = st.container()
with page_container:
    st.markdown('<div class="page-container">', unsafe_allow_html=True)

    if st.session_state.page == "home":
        st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>"
                    "<div style=''>"
                    "<h1 style='margin:0 0 4px 0;'>🍎 Welcome to Streamlit OS</h1>"
                    "<div class='small-muted'>Apple-inspired multiplatform UI — native Streamlit layout.</div>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True)

        # Cards grid implemented with native columns to avoid HTML layout issues.
        # We'll render 3 columns per row on wide screens using Streamlit columns.
        # For responsiveness, use width-based column creation.
        # Build cards as st.markdown blocks (still native).
        cards = [
            ("Page 1 — Overview", "Intro, value proposition and product highlights.", "page1"),
            ("Page 2 — Analytics", "Dashboards, charts and KPIs.", "page2"),
            ("Page 3 — Reports", "Exportable reports & tables.", "page3"),
            ("Page 4 — Collaboration", "Team boards, comments and shared views.", "page4"),
            ("Page 5 — Settings", "Profile, preferences and integrations.", "page5"),
        ]

        # Render 3-per-row responsive-ish using columns
        cols_per_row = 3
        for i in range(0, len(cards), cols_per_row):
            row = cards[i : i + cols_per_row]
            cols = st.columns(len(row))
            for c, card in zip(cols, row):
                title, desc, key = card
                with c:
                    st.markdown(f"""
                    <div class="card">
                      <div class="card-title">{title}</div>
                      <div class="card-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # native navigation button under the card
                    if st.button("Open", key=f"open_{key}"):
                        navigate(key)

    elif st.session_state.page == "page1":
        st.header("Page 1 — Overview")
        st.write("This page contains an overview of the product, value proposition, and primary features.")
        st.markdown("---")
        st.subheader("Highlights")
        st.write("- Clean minimal design inspired by Apple")
        st.write("- Focus on whitespace, typography, and smooth micro-interactions")
        st.markdown('<div style="margin-top:12px;"><button class="nav-btn" onclick="document.location=\'\'"> </button></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"):
            navigate("home")

    elif st.session_state.page == "page2":
        st.header("Page 2 — Analytics")
        st.write("Interactive analytics. Below is a sample chart created natively using Altair for smooth integration.")
        # Example: sample Altair chart (native)
        import pandas as pd
        import altair as alt
        df = pd.DataFrame({
            "month": ["Jan","Feb","Mar","Apr","May","Jun"],
            "value": [10, 15, 9, 20, 23, 18]
        })
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="month",
            y="value"
        ).properties(width="container", height=360)
        st.altair_chart(chart, use_container_width=True)
        st.markdown("")
        if st.button("← Back to Home"):
            navigate("home")

    elif st.session_state.page == "page3":
        st.header("Page 3 — Reports")
        st.write("Downloadable reports and export options.")
        st.markdown("### Sample table")
        import pandas as pd
        df = pd.DataFrame({
            "Name": ["Alice","Bob","Charlie"],
            "Metric A": [12, 9, 14],
            "Metric B": [7, 11, 5]
        })
        st.dataframe(df, use_container_width=True, height=240)
        st.markdown("")
        if st.button("← Back to Home"):
            navigate("home")

    elif st.session_state.page == "page4":
        st.header("Page 4 — Collaboration")
        st.write("Team tools: comments, shared boards, and simple message area implemented with native widgets.")
        st.text_input("Post a quick note", key="collab_note")
        if st.button("Save Note"):
            st.success("Note saved (session-only)")
        st.markdown("")
        if st.button("← Back to Home"):
            navigate("home")

    elif st.session_state.page == "page5":
        st.header("Page 5 — Settings")
        st.write("User preferences and integrations.")
        # native theme selector here, mirrors top toggle
        theme_sel = st.radio("Select theme (native)", options=["light", "dark"], index=0 if st.session_state.theme=="light" else 1)
        if theme_sel != st.session_state.theme:
            st.session_state.theme = theme_sel
            st.experimental_rerun()
        st.markdown("")
        if st.button("← Back to Home"):
            navigate("home")

    else:
        st.info("Page not found — returning home.")
        if st.button("Return to home"):
            navigate("home")

    st.markdown("</div>", unsafe_allow_html=True)  # close page-container

# --- Footer (keeps consistent height footprint) ---
with st.container():
    st.markdown("""<div style="margin-top:6px; padding:10px 6px; font-size:13px; color:gray;">Made with ❤️ — Streamlit native layout (no iframe)</div>""", unsafe_allow_html=True)
