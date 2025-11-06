import streamlit as st

# --- 1. CONFIGURATION AND STYLING (MIMICKING APPLE/TAILWIND) ---

# The core CSS block to inject. This sets the dark mode theme, 
# uses the Inter font, and provides custom classes for all components.
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
        margin: 0 auto 3rem auto;
    }
    
    .apple-page-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* 3. NEW Horizontal Navigation Bar */
    .apple-nav-container {
        width: 100%;
        border-bottom: 1px solid #2a2a2a; /* Subtle separator */
        margin-bottom: 3rem;
        padding: 0.5rem 0;
        background-color: #101010; /* Dark "strip" background */
        border-radius: 12px;  /* <-- RE-ADDED as requested */
    }
    
    /* Style for ALL buttons within the nav */
    .apple-nav-container [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        color: #888888 !important; /* Inactive link color */
        padding: 5px 10px !important;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
        width: 100%;
        transition: color 0.2s;
    }

    /* Hover state for INACTIVE buttons */
    .apple-nav-container [data-testid="stButton"] > button:not(:disabled):hover {
        color: #FFFFFF !important; /* White on hover */
        background: none !important;
        border: none !important;
    }
    
    /* Style for the *disabled* (active) button */
    .apple-nav-container [data-testid="stButton"] > button:disabled {
        font-weight: 600; /* Bolder */
        color: #FFFFFF !important; /* Active link color (White) */
        background: none !important;
        border: none !important;
        cursor: default !important;
        opacity: 1 !important; /* <-- ADDED to ensure visibility */
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

def create_main_navbar():
    """Creates the static horizontal navigation bar."""
    st.markdown('<div class="apple-nav-container">', unsafe_allow_html=True)
    cols = st.columns(6)
    
    page_keys = list(PAGE_NAMES.keys())
    page_values = list(PAGE_NAMES.values())
    
    # Iterate to create all 6 buttons
    for i in range(6):
        with cols[i]:
            is_active = (st.session_state.current_page == page_values[i])
            
            # We create a button for every link.
            # The active link is just a *disabled* button.
            # This guarantees perfect alignment.
            if st.button(page_keys[i], key=f"nav_{page_values[i]}", disabled=is_active):
                navigate_to(page_values[i])
                st.rerun() # Use rerun for instant page switch

    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PAGE CONTENT FUNCTIONS ---

def main_page():
    """The main landing page with the hero section."""
    create_main_navbar()
    st.markdown('<div class="apple-hero-title">Introducing a New Era of Innovation.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="apple-hero-subtitle">Experience seamless integration, revolutionary performance, and timeless design across all our platforms.</p>',
        unsafe_allow_html=True
    )


def page_a():
    """Vision Pro Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Apple Vision Pro</h1>', unsafe_allow_html=True)
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


def page_b():
    """MacBook Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">MacBook Pro M4</h1>', unsafe_allow_html=True)
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


def page_c():
    """iPhone 16 Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">iPhone 16 Pro</h1>', unsafe_allow_html=True)
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


def page_d():
    """Watch X Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Apple Watch X</h1>', unsafe_allow_html=True)
    st.markdown("## Reimagined. Revolutionary.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        Apple Watch X features an all-new design with a thinner case and a magnetic band attachment system. 
        It’s the essential tool for a healthy and active life.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**S10 Chip:** Faster, more efficient processing.</li>
            <li>**Blood Glucose Monitoring:** Non-invasive monitoring capability.</li>
            <li>**New Health Sensors:** Advanced crash-detection.</li>
        </ul>
    """, unsafe_allow_html=True)

    
def page_e():
    """AirPods Max Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">AirPods Max (Gen 2)</h1>', unsafe_allow_html=True)
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
