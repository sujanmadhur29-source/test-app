import streamlit as st
import time

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
        margin: 0 auto 3rem auto;
    }
    
    .apple-page-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* 3. Card/Navigation Styling (Minimalist) - Kept for future use if needed */
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
    
    /* 4. Default Button Styling (Pill shape) - Now used for nav */
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
    
    /* 5. NEW Horizontal Navigation Bar */
    .apple-nav-container {
        width: 100%;
        border-bottom: 1px solid #2a2a2a; /* Subtle separator */
        margin-bottom: 3rem;
        padding: 0.5rem 0; /* Updated padding */
        background-color: #101010; /* Dark "strip" background */
        border-radius: 12px; /* Rounded corners */
    }
    
    /* Style for the buttons within the nav */
    .apple-nav-container [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        color: #888888 !important; /* Inactive link color */
        padding: 5px 10px !important;
        font-size: 0.95rem; /* Slightly smaller */
        font-weight: 500;
        text-align: center;
        width: 100%;
    }

    .apple-nav-container [data-testid="stButton"] > button:hover {
        color: #FFFFFF !important; /* White on hover */
        background: none !important;
        border: none !important;
    }
    
    /* Style for the *disabled* (active) button */
    .apple-nav-container [data-testid="stButton"] > button:disabled {
        font-weight: 600; /* Bolder */
        color: #FFFFFF !important; /* Active link color */
        background: none !important;
        border: none !important;
        cursor: default !important;
    }

    /* 6. Form Element Styling */
    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stTextArea"] > div > div > textarea {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 8px; /* Slightly less rounded than pills */
        padding: 12px 15px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stTextArea"] > div > div > textarea {
        min-height: 100px; /* Specific to text area */
    }

    /* Style for text input labels */
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label {
        color: #AAAAAA;
        font-weight: 500;
        padding-bottom: 5px;
    }

    /* 7. Primary Action Button (for 'Generate') - Primary Style */
    .apple-primary-button-container div.stButton > button {
        background-color: #007AFF !important; /* Apple Blue */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9999px; /* Pill shape */
        padding: 12px 28px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: background-color 0.2s;
        width: auto; /* Allow it to size to content */
        margin-top: 1.5rem;
    }
    
    .apple-primary-button-container div.stButton > button:disabled {
        background: #333 !important; /* Disabled grey */
        color: #888 !important;
        border: none !important;
    }

    .apple-primary-button-container div.stButton > button:hover {
        background-color: #0056b3 !important; /* Darker blue on hover */
        color: #FFFFFF !important;
        border: none !important;
    }
    
    /* 8. Input Summary Styling */
    .input-summary-section {
        background-color: #101010; /* Darker than output */
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .input-summary-section h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #AAAAAA; /* Grey label */
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .input-summary-section p {
        font-size: 1.1rem;
        color: #E0E0E0;
        line-height: 1.6;
        font-style: italic;
        /* Use pre-wrap to respect newlines in the input */
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* 9. Output Display Styling */
    .brand-output-section {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-top: 2rem;
        border: 1px solid #2a2a2a;
    }

    .brand-output-section h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFFFFF;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .brand-output-section p {
        font-size: 1rem;
        color: #E0E0E0;
        line-height: 1.6;
    }
    
    .brand-output-section pre {
        white-space: pre-wrap; /* Ensure text wraps */
        word-wrap: break-word; /* Break long words */
        background-color: #080808; /* Slightly darker */
        padding: 1.5rem;
        border-radius: 8px;
        color: #E0E0E0;
        font-family: 'Menlo', 'Consolas', monospace;
        font-size: 0.95rem;
        line-height: 1.7;
    }


    /* Hide default Streamlit Chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# Apply the custom CSS at the start
st.set_page_config(layout="wide", page_title="Brand Generator App")
st.markdown(APPLE_TAILWIND_CSS, unsafe_allow_html=True)


# --- 2. STATE AND NAVIGATION FUNCTIONS ---

PAGE_NAMES = {
    "Home": "main_page",
    "Branding": "page_a", # Renamed from "Vision Pro"
    "MacBook": "page_b",
    "iPhone 16": "page_c",
    "Watch X": "page_d",
    "AirPods Max": "page_e",
}

# Initialize session state for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]
if 'startup_idea' not in st.session_state:
    st.session_state.startup_idea = None
if 'startup_values' not in st.session_state:
    st.session_state.startup_values = None
if 'generating' not in st.session_state:
    st.session_state.generating = False

def navigate_to(page_key):
    """Sets the current page in session state."""
    st.session_state.current_page = page_key

def create_main_navbar():
    """Creates the static horizontal navigation bar."""
    st.markdown('<div class="apple-nav-container">', unsafe_allow_html=True)
    cols = st.columns(6)
    
    page_keys = list(PAGE_NAMES.keys()) # ["Home", "Branding", ...]
    page_values = list(PAGE_NAMES.values()) # ["main_page", "page_a", ...]
    
    with cols[0]:
        is_active = st.session_state.current_page == page_values[0]
        if st.button(page_keys[0], key="nav_home", disabled=is_active):
            navigate_to(page_values[0])
            st.rerun() # Use rerun for instant page switch
    
    with cols[1]:
        is_active = st.session_state.current_page == page_values[1]
        if st.button(page_keys[1], key="nav_branding", disabled=is_active): # Updated key
            navigate_to(page_values[1])
            st.rerun()
                
    with cols[2]:
        is_active = st.session_state.current_page == page_values[2]
        if st.button(page_keys[2], key="nav_mac", disabled=is_active):
            navigate_to(page_values[2])
            st.rerun()

    with cols[3]:
        is_active = st.session_state.current_page == page_values[3]
        if st.button(page_keys[3], key="nav_iphone", disabled=is_active):
            navigate_to(page_values[3])
            st.rerun()
                
    with cols[4]:
        is_active = st.session_state.current_page == page_values[4]
        if st.button(page_keys[4], key="nav_watch", disabled=is_active):
            navigate_to(page_values[4])
            st.rerun()
                
    with cols[5]:
        is_active = st.session_state.current_page == page_values[5]
        if st.button(page_keys[5], key="nav_airpods", disabled=is_active):
            navigate_to(page_values[5])
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PAGE CONTENT FUNCTIONS ---

def main_page():
    """The main landing page with the hero section and input form."""
    create_main_navbar()
    st.markdown('<div class="apple-hero-title">Introducing a New Era of Innovation.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="apple-hero-subtitle">First, let\'s define your brand. Start by describing your vision.</p>',
        unsafe_allow_html=True
    )
    
    # --- New Input Form ---
    with st.form(key="brand_form"):
        idea = st.text_area(
            "What idea do you have in mind?", 
            placeholder="e.g., A subscription service for AI-powered coding tutors",
            height=100
        )
        values = st.text_area(
            "What values are important to you?", 
            placeholder="e.g., Accessibility, Innovation, and Community",
            height=100
        )
        
        # Center the button
        st.markdown('<div class="apple-primary-button-container" style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Brand Identity", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not idea or not values:
                st.error("Please fill out both fields to generate your brand identity.")
            else:
                st.session_state.startup_idea = idea
                st.session_state.startup_values = values
                st.session_state.generating = True # Flag to show spinner on next page
                navigate_to(PAGE_NAMES["Branding"]) # Navigate to new page name
                st.rerun()


# --- Mock Generation and Prompt Template ---

def get_mock_brand_output(idea, values):
    """
    Simulates a call to the Gemini API and returns a formatted string.
    """
    # Use the inputs to make the mock data feel dynamic
    # Pick one name to be consistent
    name_idea = idea.split(' ')[0].capitalize() if idea else "Innovate"
    selected_name = f"{name_idea}Sphere"
    selected_tagline = f"Innovate for {values.split(',')[0]}."

    # This simulates the formatted output from the LLM
    mock_output = f"""
**1. Brand Name:** {selected_name}\n
**Tagline:** {selected_tagline}\n
**Tone/Meaning Explanation:** Combines '{name_idea}' (from your idea: {idea[:20]}...) and 'Sphere' (global, holistic), suggesting a brand focused on your values.\n

**2. Brand Name:** TerraPact\n
**Tagline:** Built on {values}.\n
**Tone/Meaning Explanation:** 'Terra' (Earth) + 'Pact' (promise). A strong, trustworthy name that commits to its values, inspired by your idea: "{idea[:20]}...".\n

**3. Brand Name:** Kinetix Core\n
**Tagline:** The {values.split(' ')[-1]} of Motion.\n
**Tone/Meaning Explanation:** 'Kinetix' (energy, movement) + 'Core' (central, essential). This name sounds innovative and fundamental, perfect for a tech-driven startup.\n

---

**Logo Concept Prompt:**
“Design a logo for {selected_name}. The style should be modern and minimalist, feature a color palette inspired by {values} (e.g., earth tones like green, blue, and sand), and use imagery/symbols that reflect a fusion of technology and nature (like a stylized leaf forming a circuit or a clean, abstract globe). The emotional tone should convey trust, innovation, and sustainability.”

---

**Poster Design Prompt:**
“Create a visually engaging poster for {selected_name}, featuring the tagline '{selected_tagline}'. The poster should feature a subtle, abstract representation of a circuit board pattern merging with a natural landscape, use colors and typography consistent with {values} (deep greens, sky blues, and a clean, sans-serif font), and display imagery that aligns with the startup’s mission of '{idea[:30]}...'. The overall vibe should be aspirational, clean, and futuristic. Use a sleek, graphic illustration style.”
"""
    return mock_output


def page_a():
    """Branding Page / Brand Output Page"""
    create_main_navbar()
    
    # Check if we landed here from the form
    if st.session_state.startup_idea and st.session_state.startup_values:
        st.markdown('<h1 class="apple-page-title">Your Brand Identity</h1>', unsafe_allow_html=True)
        
        # Display the inputs
        st.markdown(f"""
        <div class="input-summary-section">
            <h3>Startup Idea</h3>
            <p>"{st.session_state.startup_idea}"</p>
            <h3 style="margin-top: 1rem;">Values</h3>
            <p>"{st.session_state.startup_values}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        output_placeholder = st.empty()
        
        if st.session_state.generating:
            with st.spinner("Generating your brand..."):
                time.sleep(2) # Simulate API call time
                brand_output = get_mock_brand_output(
                    st.session_state.startup_idea, 
                    st.session_state.startup_values
                )
                st.session_state.brand_output = brand_output # Store output
                st.session_state.generating = False # Done generating
        
        # Display the generated output
        if 'brand_output' in st.session_state:
            output_placeholder.markdown(
                f'<div class="brand-output-section"><pre>{st.session_state.brand_output}</pre></div>', 
                unsafe_allow_html=True
            )
        
        # Clear the inputs so refreshing the page doesn't re-run
        # You might want to remove these lines if you want the data to persist
        # st.session_state.startup_idea = None
        # st.session_state.startup_values = None
        
    else:
        # Original "Branding" page content (was "Vision Pro")
        st.markdown('<h1 class="apple-page-title">Branding</h1>', unsafe_allow_html=True)
        st.markdown("## Define Your Identity.")
        st.markdown("""
            <p style="font-size: 1.1rem; color: #E0E0E0;">
            This is where your brand comes to life. A strong brand identity seamlessly blends your mission
            with your values, creating a memorable experience for your audience.
            </p>
            <p style="font-size: 1.1rem; color: #AAAAAA; margin-top: 2rem;">
            <i>To generate a brand identity, please return to the <b>Home</b> page and fill out the form.</i>
            </p>
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
    PAGE_NAMES["Branding"]: page_a, # Updated
    PAGE_NAMES["MacBook"]: page_b,
    PAGE_NAMES["iPhone 16"]: page_c,
    PAGE_NAMES["Watch X"]: page_d,
    PAGE_NAMES["AirPods Max"]: page_e,
}

# Execute the function corresponding to the current page state
page_functions[st.session_state.current_page]()
