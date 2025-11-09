
import streamlit as st
import time
import google.generativeai as genai
import os

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

    /* NEW: Style for placeholders */
    [data-testid="stTextInput"] > div > div > input::placeholder,
    [data-testid="stTextArea"] > div > div > textarea::placeholder {
        color: #777777;
        font-size: 0.9rem;
        font-style: italic;
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
        color: #FFFFFF !important;
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
        word-wrap: break-word; /* Added for long string wrapping */
        overflow-wrap: break-word; /* Added for long string wrapping */
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
    
    /* NEW: Styling for markdown generated by the new prompt */
    .brand-output-section h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
    }
    
    .brand-output-section h4 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E0E0E0;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .brand-output-section ul {
        list-style-type: disc;
        margin-left: 20px;
        padding-left: 0;
        color: #E0E0E0;
    }
    
    .brand-output-section li {
        margin-bottom: 0.5rem;
        line-height: 1.6;
        word-wrap: break-word; /* Added for long string wrapping */
        overflow-wrap: break-word; /* Added for long string wrapping */
    }

    .brand-output-section img {
        border-radius: 8px;
        margin-top: 1rem;
        max-width: 300px;
        border: 1px solid #333;
    }

    /* NEW: Styling for tables to prevent overflow */
    .brand-output-section table {
        display: block; /* Makes the table scrollable */
        width: 100%;
        overflow-x: auto; /* Adds horizontal scroll if needed */
        border-collapse: collapse;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #333; /* Border to match theme */
        border-radius: 8px; /* Match other elements */
    }

    .brand-output-section th,
    .brand-output-section td {
        border-bottom: 1px solid #333; /* Cell borders */
        padding: 0.75rem 1rem; /* Spacing */
        color: #E0E0E0;
        white-space: nowrap; /* Prevents text from wrapping and breaking layout */
        border-left: 1px solid #333;
    }
    
    .brand-output-section td:first-child,
    .brand-output-section th:first-child {
        border-left: none; /* Remove double border on the left */
    }

    .brand-output-section th {
        background-color: #2a2a2a; /* Header background */
        font-weight: 600;
        text-align: left;
    }
    
    .brand-output-section tr:first-child th:first-child {
        border-top-left-radius: 7px; /* Rounded corner */
    }
    .brand-output-section tr:first-child th:last-child {
        border-top-right-radius: 7px; /* Rounded corner */
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

# --- 2. GEMINI API CONFIGURATION ---

# Configure the API key from Streamlit secrets
try:
    # API_KEY = st.secrets["GEMINI_API_KEY"] # Replaced secret with hardcoded key
    API_KEY = "AIzaSyDkoQ2M7c7EcUFpLBTMvFlAXjMg1f2TUHI"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    GEMINI_ENABLED = True
except Exception as e:
    # Updated error message
    st.error(f"Error configuring Gemini API: {e}. Please check the API key.")
    GEMINI_ENABLED = False

# The prompt template to be filled by user inputs
SEGMENTATION_PROMPT_TEMPLATE = """
You are a Startup Market Segmentation Expert with access to generative tools and data APIs.

---
### USER INPUTS
* **Startup Idea:** {idea}
* **Launch Plan:** {launch_plan}
---

Based on these inputs, generate a detailed market segmentation analysis.

### Your objectives:
1. Generate detailed target market and customer segmentation for the startup’s product idea.
2. Output both analytical and creative persona details. **IMPORTANT: For the 'Generated Persona Image', do NOT generate an image. Instead, use a descriptive placeholder URL from 'https://placehold.co/300x300/E0E0E0/000000?text=Persona+Name'**, replacing 'Persona+Name' with the actual persona's name (e.g., Aarav+K).

---
### Step 1: Primary Target Market
Write one crisp sentence defining:
* The broad target market (country, demographics, psychographic need) based on the user's inputs.
---
### Step 2: Customer Segments (3–5)
For each segment, provide:
* **Segment Name:** Catchy but descriptive
* **Demographics:** Age, gender, income, geography
* **Psychographics:** Values, attitudes, lifestyle
* **Buying Motivations:** Key reasons to purchase
* **Pain Points / Unmet Needs:**
* **Channels & Media Preferences:** (Instagram, Blinkit, Zomato, LinkedIn, etc.)
* **Price Sensitivity:** High / Medium / Low
* **Fit with Brand:** High / Medium / Low
* **Persona Summary:** ≤80 words; written like a short story about this person’s daily life
* **Generated Persona Image:** [Use the https://placehold.co URL as specified in the objectives]
Use realistic, India-specific details and current digital behavior cues based on the user's inputs.
---
### Step 3: Segment Prioritization
* Identify 1–2 high-priority segments to target first, and justify clearly.
* **Suggest the key marketing message or value proposition for them.**
---
### Step 4: Positioning Implication
* Define how the brand should position itself to attract these top segments.
* Suggest tone of voice and visual style cues for creatives.
---
### Step 5: Risks / Overlooked Audiences
* Highlight blind spots, compliance or regulatory concerns (e.g., FSSAI for beverages), and emerging opportunities.
---
### Step 6: Output Formatting
Return your answer using clean, readable Markdown (headings, bullets) for clarity and embed the placeholder image URLs directly.
---
### Constraints
* Keep it concise, practical, and realistic to the Indian market.
* Use INR and Asia/Kolkata context.
* Avoid generic phrasing; show behavioral, digital, and cultural nuance relevant to the user's idea.
"""


# --- 3. STATE AND NAVIGATION FUNCTIONS ---

PAGE_NAMES = {
    "Home": "main_page",
    "Segment View": "page_a", # Renamed from "Branding"
    "Target Lens": "page_b", # Renamed from "MacBook"
    "Market Radar": "page_c", # Renamed from "iPhone 16"
    "Roadmap": "page_d", # Renamed from "Watch X"
    "Pricing": "page_e", # Renamed from "AirPods Max"
}

# Initialize session state for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]
if 'startup_idea' not in st.session_state:
    st.session_state.startup_idea = None
# Renamed startup_values to startup_launch_plan for clarity
if 'startup_launch_plan' not in st.session_state:
    st.session_state.startup_launch_plan = None
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
        if st.button(page_keys[1], key="nav_branding", disabled=is_active): # Updated key (key name is internal, fine to keep)
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
            placeholder="What is your product or service? What makes your product unique? How will you sell it?",
            height=100
        )
        # Updated this section as requested
        launch_plan = st.text_area(
            "What are your thoughts on a launch plan?", 
            placeholder="Where are you launching first? Who is your ideal customer? Any constraints?",
            height=100
        )
        
        # Center the button
        st.markdown('<div class="apple-primary-button-container" style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Brand Identity", type="primary", disabled=not GEMINI_ENABLED)
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not idea or not launch_plan:
                st.error("Please fill out both fields to generate your brand identity.")
            else:
                st.session_state.startup_idea = idea
                st.session_state.startup_launch_plan = launch_plan # Updated state variable
                st.session_state.generating = True # Flag to show spinner on next page
                navigate_to(PAGE_NAMES["Segment View"]) # FIXED: Was "Branding"
                st.rerun()


# --- 4. GEMINI API CALL FUNCTION ---

def call_gemini_api(idea, launch_plan):
    """
    Calls the Gemini API with the formatted segmentation prompt.
    """
    if not GEMINI_ENABLED:
        return "Error: Gemini API is not configured. Please check your API key."

    # Format the prompt with user inputs
    prompt = SEGMENTATION_PROMPT_TEMPLATE.format(idea=idea, launch_plan=launch_plan)
    
    try:
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return f"Error: Could not generate content. {e}"


# --- 5. PAGE CONTENT FUNCTIONS ---

def page_a():
    """Segment View Page / Brand Output Page"""
    create_main_navbar()
    
    # Check if we landed here from the form
    if st.session_state.startup_idea and st.session_state.startup_launch_plan:
        st.markdown('<h1 class="apple-page-title">Your Brand Identity</h1>', unsafe_allow_html=True)
        
        # Display the inputs
        st.markdown(f"""
        <div class="input-summary-section">
            <h3>Startup Idea</h3>
            <p>"{st.session_state.startup_idea}"</p>
            <h3 style="margin-top: 1rem;">Launch Plan</h3>
            <p>"{st.session_state.startup_launch_plan}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        output_placeholder = st.empty()
        
        if st.session_state.generating:
            with st.spinner("Calling Gemini to generate your brand identity..."):
                # Replaced mock function with live API call
                segmentation_output = call_gemini_api(
                    st.session_state.startup_idea, 
                    st.session_state.startup_launch_plan
                )
                st.session_state.segmentation_output = segmentation_output # Store output
                st.session_state.generating = False # Done generating
        
        # Display the generated output
        if 'segmentation_output' in st.session_state:
            # Render as Markdown, not in a <pre> tag
            output_placeholder.markdown(
                f'<div class="brand-output-section">{st.session_state.segmentation_output}</div>', 
                unsafe_allow_html=True
            )
        
        # Clear the inputs so refreshing the page doesn't re-run
        # You might want to remove these lines if you want the data to persist
        # st.session_state.startup_idea = None
        # st.session_state.startup_launch_plan = None
        
    else:
        # Original "Branding" page content (was "Vision Pro")
        st.markdown('<h1 class="apple-page-title">Segment View</h1>', unsafe_allow_html=True)
        st.markdown("## Define Your Identity.")
        st.markdown("""
            <p style="font-size: 1.1rem; color: #AAAAAA; margin-top: 2rem;">
            <i>To generate a brand identity, please return to the <b>Home</b> page and fill out the form.</i>
            </p>
        """, unsafe_allow_html=True)


def page_b():
    """Target Lens Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Target Lens</h1>', unsafe_allow_html=True)
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
    """Market Radar Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Market Radar</h1>', unsafe_allow_html=True)
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
    """Roadmap Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Roadmap</h1>', unsafe_allow_html=True)
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
    """Pricing Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Pricing</h1>', unsafe_allow_html=True)
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


# --- 6. MAIN APPLICATION LOGIC ---

page_functions = {
    PAGE_NAMES["Home"]: main_page,
    PAGE_NAMES["Segment View"]: page_a, # Updated
    PAGE_NAMES["Target Lens"]: page_b, # Updated
    PAGE_NAMES["Market Radar"]: page_c, # Updated
    PAGE_NAMES["Roadmap"]: page_d, # Updated
    PAGE_NAMES["Pricing"]: page_e, # Updated
}

# Execute the function corresponding to the current page state
page_functions[st.session_state.current_page]()
