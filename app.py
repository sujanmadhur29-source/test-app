import streamlit as st

# --- 1. CONFIGURATION AND STYLING (MIMICKING APPLE/TAILWIND) ---

# The core CSS block to inject. This sets the dark mode theme, 
# uses the Inter font (a common choice for modern, clean UI), 
# and provides custom classes for the Apple-like components.
APPLE_TAILWIND_CSS = """
<style>
    /* 1. Global Setup (Dark Mode and Font) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000; /* Pure Black for contrast */
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Center the main container content and maximize width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px !important;
    }

    /* 2. Custom Typography and Layout */
    .apple-hero-title {
        font-size: 4rem;
        font-weight: 700;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(180deg, #FFFFFF, #B0B0B0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .apple-hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        text-align: center;
        color: #888888;
        /* max-width: 600px; <-- REMOVED this line to allow full width extension */
        margin: 0 auto 3rem auto;
    }
    
    .apple-page-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* 3. Card/Navigation Styling (Minimalist) */
    .apple-card {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        cursor: pointer;
    }
    
    .apple-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
    }
    
    .apple-card h3 {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .apple-card p {
        color: #AAAAAA;
        font-size: 1rem;
    }

    /* 4. Button Styling (Clean and Rounded) */
    div.stButton > button {
        background-color: #1a1a1a; 
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 9999px; /* Pill shape */
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: 500;
        transition: background-color 0.2s, border-color 0.2s;
        cursor: pointer;
    }

    div.stButton > button:hover {
        background-color: #333333;
        border-color: #555555;
    }

    /* Hide default Streamlit Chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# Apply the custom CSS at the start
st.set_page_config(layout="wide", page_title="Apple-Inspired Streamlit App")
st.markdown(APPLE_TAILWIND_CSS, unsafe_allow_html=True)


# --- 2. STATE AND NAVIGATION FUNCTIONS ---

PAGE_NAMES = {
    "Home": "main_page",
    "Vision Pro": "page_a",
    "MacBook": "page_b",
    "iPhone 16": "page_c",
    "Watch X": "page_d",
    "AirPods Max": "page_e",
}

# Initialize session state for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]

def navigate_to(page_key):
    """Sets the current page in session state."""
    st.session_state.current_page = page_key

def create_navigation_button():
    """Renders the "Back to Home" button used on all sub-pages."""
    if st.session_state.current_page != PAGE_NAMES["Home"]:
        st.markdown(
            '<div style="text-align: center; margin-top: 40px;">', 
            unsafe_allow_html=True
        )
        # Use a standard Streamlit button and let the CSS style it
        if st.button("← Back to Home"):
            navigate_to(PAGE_NAMES["Home"])
        st.markdown('</div>', unsafe_allow_html=True)


# --- 3. PAGE CONTENT FUNCTIONS ---

def main_page():
    """The main landing page with the hero section and navigation grid."""
    st.markdown('<div class="apple-hero-title">Introducing a New Era of Innovation.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="apple-hero-subtitle">Experience seamless integration, revolutionary performance, and timeless design across all our platforms.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    
    # Use Streamlit columns for the grid layout
    cols = st.columns(3)
    
    # Navigation Cards (Page A and B)
    with cols[0]:
        st.markdown(
            f'<div class="apple-card" onclick="document.getElementById(\'nav-vision-pro\').click()"><h3>{list(PAGE_NAMES.keys())[1]}</h3><p>Spatial computing. Now available.</p></div>',
            unsafe_allow_html=True
        )
        # Wrap the functional button in a hidden div to ensure reliable navigation without visual clutter
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        if st.button("Navigate to Vision Pro", key="nav-vision-pro"):
            navigate_to(PAGE_NAMES["Vision Pro"])
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown(
            f'<div class="apple-card" onclick="document.getElementById(\'nav-macbook\').click()"><h3>{list(PAGE_NAMES.keys())[2]}</h3><p>M4 Pro. Unleash Pro performance.</p></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        if st.button("Navigate to MacBook", key="nav-macbook"):
            navigate_to(PAGE_NAMES["MacBook"])
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[2]:
        st.markdown(
            f'<div class="apple-card" onclick="document.getElementById(\'nav-iphone\').click()"><h3>{list(PAGE_NAMES.keys())[3]}</h3><p>Capture. Create. Connect. Better.</p></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        if st.button("Navigate to iPhone 16", key="nav-iphone"):
            navigate_to(PAGE_NAMES["iPhone 16"])
        st.markdown('</div>', unsafe_allow_html=True)
            
    # Navigation Cards (Page D and E)
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown(
            f'<div class="apple-card" onclick="document.getElementById(\'nav-watch\').click()"><h3>{list(PAGE_NAMES.keys())[4]}</h3><p>The future of health is on your wrist.</p></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        if st.button("Navigate to Watch X", key="nav-watch"):
            navigate_to(PAGE_NAMES["Watch X"])
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown(
            f'<div class="apple-card" onclick="document.getElementById(\'nav-airpods\').click()"><h3>{list(PAGE_NAMES.keys())[5]}</h3><p>Redesigned for pure, immersive audio.</p></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        if st.button("Navigate to AirPods Max", key="nav-airpods"):
            navigate_to(PAGE_NAMES["AirPods Max"])
        st.markdown('</div>', unsafe_allow_html=True)
            
    # Empty column for alignment
    with cols[2]:
        st.markdown(
            '<div class="apple-card" style="opacity: 0.2; cursor: default;"><h3>More Coming Soon</h3><p>Stay tuned for our next groundbreaking product.</p></div>',
            unsafe_allow_html=True
        )

    # REMOVED the problematic global CSS block that hid all buttons.


def page_a():
    """Vision Pro Page"""
    st.markdown('<h1 class="apple-page-title">Apple Vision Pro</h1>', unsafe_allow_html=True)
    st.image("https://placehold.co/1000x500/0A0A0A/E0E0E0?text=Vision+Pro+Demo", use_column_width=True)
    st.markdown("## Spatial Computing is Here.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        Vision Pro seamlessly blends digital content with your physical world. You can navigate the world with your eyes, hands, and voice. 
        It’s a revolutionary way to work, communicate, and enjoy entertainment.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**Optic ID:** Advanced security that analyzes your iris.</li>
            <li>**R1 Chip:** Processes input from 12 cameras, five sensors, and six microphones.</li>
            <li>**3D Camera:** Capture spatial photos and videos.</li>
        </ul>
    """, unsafe_allow_html=True)
    create_navigation_button()


def page_b():
    """MacBook Page"""
    st.markdown('<h1 class="apple-page-title">MacBook Pro M4</h1>', unsafe_allow_html=True)
    st.image("https://placehold.co/1000x500/0A0A0A/E0E0E0?text=MacBook+Pro+M4", use_column_width=True)
    st.markdown("## Power. Efficiency. Pro.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        The MacBook Pro, supercharged by the M4 chip, delivers a staggering leap in performance and battery life. 
        It is the ultimate notebook for professional creators and developers.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**Liquid Retina XDR:** The best display ever in a notebook.</li>
            <li>**Neural Engine:** 16-core, for advanced machine learning tasks.</li>
            <li>**Up to 22 Hours:** Unprecedented battery life on a single charge.</li>
        </ul>
    """, unsafe_allow_html=True)
    create_navigation_button()

def page_c():
    """iPhone 16 Page"""
    st.markdown('<h1 class="apple-page-title">iPhone 16 Pro</h1>', unsafe_allow_html=True)
    st.image("https://placehold.co/1000x500/0A0A0A/E0E0E0?text=iPhone+16+Pro", use_column_width=True)
    st.markdown("## A Giant Leap for Photography.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        The new camera system in iPhone 16 Pro brings light and detail to your images like never before. 
        The Action button and USB-C port simplify everything.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**A18 Bionic Chip:** Faster performance, superior gaming.</li>
            <li>**ProMotion Display:** Adaptive 120Hz refresh rate.</li>
            <li>**48MP Main Camera:** Unrivaled low-light performance.</li>
        </ul>
    """, unsafe_allow_html=True)
    create_navigation_button()

def page_d():
    """Watch X Page"""
    st.markdown('<h1 class="apple-page-title">Apple Watch X</h1>', unsafe_allow_html=True)
    st.image("https://placehold.co/1000x500/0A0A0A/E0E0E0?text=Apple+Watch+X", use_column_width=True)
    st.markdown("## Reimagined. Revolutionary.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        Apple Watch X features an all-new design with a thinner case and a magnetic band attachment system. 
        It’s the essential tool for a healthy and active life.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**S10 Chip:** Faster, more efficient processing.</li>
            <li>**Blood Glucose Monitoring:** Non-invasive monitoring capability.</li>
            <li>**New Health Sensors:** Advanced crash and fall detection.</li>
        </ul>
    """, unsafe_allow_html=True)
    create_navigation_button()
    
def page_e():
    """AirPods Max Page"""
    st.markdown('<h1 class="apple-page-title">AirPods Max (Gen 2)</h1>', unsafe_allow_html=True)
    st.image("https://placehold.co/1000x500/0A0A0A/E0E0E0?text=AirPods+Max+Gen+2", use_column_width=True)
    st.markdown("## Audio Purity. Redefined.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        AirPods Max deliver unparalleled high-fidelity audio with industry-leading Active Noise Cancellation. 
        They've been updated with USB-C and extended battery life.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**H3 Chip:** Advanced computational audio processing.</li>
            <li>**Lossless Audio:** Support for high-resolution lossless audio.</li>
            <li>**New Carrying Case:** Ultra-low power mode for extended standby.</li>
        </ul>
    """, unsafe_allow_html=True)
    create_navigation_button()


# --- 4. MAIN APPLICATION LOGIC ---

page_functions = {
    PAGE_NAMES["Home"]: main_page,
    PAGE_NAMES["Vision Pro"]: page_a,
    PAGE_NAMES["MacBook"]: page_b,
    PAGE_NAMES["iPhone 16"]: page_c,
    PAGE_NAMES["Watch X"]: page_d,
    PAGE_NAMES["AirPods Max"]: page_e,
}

# Execute the function corresponding to the current page state
page_functions[st.session_state.current_page]()
