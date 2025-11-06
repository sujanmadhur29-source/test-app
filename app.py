import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Apple-Inspired Streamlit App",
    page_icon="🍎",
    layout="wide",
)

# --- TAILWIND + ANIMATIONS + DARK MODE ---
tailwind_and_style = """
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link href="https://unpkg.com/lucide-static@latest/font/lucide.css" rel="stylesheet">

<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        transition: background 0.5s ease, color 0.5s ease;
    }

    [data-theme='light'] {
        background: linear-gradient(to bottom right, #f9fafb, #ffffff);
        color: #111827;
    }
    [data-theme='dark'] {
        background: linear-gradient(to bottom right, #111827, #1f2937);
        color: #f9fafb;
    }

    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .nav-button {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        backdrop-filter: blur(8px);
        transition: all 0.25s ease;
        font-weight: 500;
    }
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }

    .apple-card {
        background: rgba(255,255,255,0.7);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .apple-card:hover {
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }

    [data-theme='dark'] .apple-card {
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 10px 25px rgba(255,255,255,0.05);
    }

    .toggle-btn {
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .toggle-btn:hover {
        transform: rotate(20deg);
    }
</style>

<script>
function toggleTheme() {
    const root = document.documentElement;
    const theme = root.getAttribute('data-theme');
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
});
</script>
"""

st.markdown(tailwind_and_style, unsafe_allow_html=True)

# --- NAVIGATION ---
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["0"])[0]


# --- NAV BAR ---
def nav_bar():
    st.markdown(
        """
        <div class="flex justify-between items-center py-4 px-8 mb-8 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center space-x-2">
                <i class="lucide lucide-apple text-2xl"></i>
                <span class="text-2xl font-semibold">Streamlit OS</span>
            </div>
            <div>
                <button class="nav-button" onclick="window.location.href='?page=0'"><i class='lucide lucide-home'></i> Home</button>
                <button class="nav-button" onclick="window.location.href='?page=1'"><i class='lucide lucide-monitor'></i> Page 1</button>
                <button class="nav-button" onclick="window.location.href='?page=2'"><i class='lucide lucide-bar-chart'></i> Page 2</button>
                <button class="nav-button" onclick="window.location.href='?page=3'"><i class='lucide lucide-file-text'></i> Page 3</button>
                <button class="nav-button" onclick="window.location.href='?page=4'"><i class='lucide lucide-users'></i> Page 4</button>
                <button class="nav-button" onclick="window.location.href='?page=5'"><i class='lucide lucide-settings'></i> Page 5</button>
            </div>
            <div onclick="toggleTheme()" class="toggle-btn">
                <i class="lucide lucide-sun text-xl dark:hidden"></i>
                <i class="lucide lucide-moon text-xl hidden dark:inline"></i>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- PAGE CONTENTS ---
def home():
    st.markdown(
        """
        <div class="fade-in text-center mt-12">
            <h1 class="text-5xl font-bold mb-4">🍎 Welcome to Streamlit OS</h1>
            <p class="text-lg text-gray-600 dark:text-gray-300 mb-12">An Apple-inspired multipage app built with Streamlit and Tailwind CSS.</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 px-16">
                <div class="apple-card">
                    <h3 class="text-xl font-semibold mb-2">Page 1 - Overview</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-4">Key features and introduction.</p>
                    <a href="?page=1" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Open →</a>
                </div>
                <div class="apple-card">
                    <h3 class="text-xl font-semibold mb-2">Page 2 - Analytics</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-4">Insights, charts and metrics.</p>
                    <a href="?page=2" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Open →</a>
                </div>
                <div class="apple-card">
                    <h3 class="text-xl font-semibold mb-2">Page 3 - Reports</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-4">Detailed data-driven reports.</p>
                    <a href="?page=3" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Open →</a>
                </div>
                <div class="apple-card">
                    <h3 class="text-xl font-semibold mb-2">Page 4 - Collaboration</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-4">Team communication tools.</p>
                    <a href="?page=4" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Open →</a>
                </div>
                <div class="apple-card">
                    <h3 class="text-xl font-semibold mb-2">Page 5 - Settings</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-4">Customize and personalize.</p>
                    <a href="?page=5" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Open →</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def simple_page(title, description):
    st.markdown(
        f"""
        <div class="fade-in mt-12 px-12">
            <h2 class="text-4xl font-semibold mb-4">{title}</h2>
            <p class="text-gray-600 dark:text-gray-300 mb-10">{description}</p>
            <a href="?page=0" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">← Back to Home</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- RENDER ---
nav_bar()

if page == "0":
    home()
elif page == "1":
    simple_page("Page 1 - Overview", "Learn about the key features and layout of this webapp.")
elif page == "2":
    simple_page("Page 2 - Analytics", "Visualize data, trends, and metrics with interactive charts.")
elif page == "3":
    simple_page("Page 3 - Reports", "Generate and export in-depth business and system reports.")
elif page == "4":
    simple_page("Page 4 - Collaboration", "Connect with your team, share insights, and manage workspaces.")
elif page == "5":
    simple_page("Page 5 - Settings", "Adjust system preferences, themes, and user options.")
else:
    home()