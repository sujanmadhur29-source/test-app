import streamlit as st
import google.generativeai as genai
import time
import re

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
        font-size: 1.25rem;
        font-weight: 400;
        color: #888888; /* Softer grey */
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .apple-page-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
        color: #FAFAFA;
    }

    /* 3. Custom Horizontal Navigation Bar (Pill Shape) */
    .apple-nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
    }
    
    .apple-nav {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #1a1a1a; /* Darker charcoal */
        border-radius: 9999px; /* Pill shape */
        padding: 0.5rem 0.75rem;
        border: 1px solid #2a2a2a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .apple-nav-item {
        background-color: transparent;
        border: none;
        color: #888888; /* Dimmed, unselected text */
        font-weight: 500;
        padding: 0.75rem 1.25rem;
        border-radius: 9999px;
        text-decoration: none;
        margin: 0 0.25rem;
        transition: all 0.3s ease;
    }
    
    .apple-nav-item:hover {
        background-color: #2a2a2a; /* Subtle hover */
        color: #FFFFFF;
    }
    
    .apple-nav-item-selected {
        background-color: #444444; /* Grey for selected item */
        color: #FFFFFF;
    }

    /* 4. Form and Input Styling */
    .brand-form-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2.5rem;
        background-color: #121212; /* Slightly lighter than pure black */
        border-radius: 12px;
        border: 1px solid #2a2a2a;
    }
    
    /* Style the placeholder text */
    ::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
      color: #555 !important; /* Lighter grey */
      opacity: 1 !important; /* Firefox */
      font-style: italic;
      font-size: 0.95rem; /* Slightly smaller */
    }

    :-ms-input-placeholder { /* Internet Explorer 10-11 */
      color: #555 !important;
      font-style: italic;
      font-size: 0.95rem;
    }

    ::-ms-input-placeholder { /* Microsoft Edge */
      color: #555 !important;
      font-style: italic;
      font-size: 0.95rem;
    }
    
    /* Make the text area labels larger */
    .stTextArea label {
        font-size: 1.15rem;
        font-weight: 600;
        color: #FAFAFA !important;
        margin-bottom: 0.5rem;
    }
    
    /* Style the text area itself */
    .stTextArea textarea {
        background-color: #1a1a1a;
        border: 1px solid #333;
        color: #FFFFFF;
        border-radius: 8px;
        min-height: 120px;
    }
    
    /* Custom Streamlit Button (Submit) */
    .stButton button {
        background-color: #007AFF; /* Apple Blue */
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        width: 100%;
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }

    /* 5. Custom Output Section Styling */
    .brand-output-section {
        margin-top: 3rem;
        padding: 2rem;
        background-color: #121212;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
    }

    .brand-output-section h1,
    .brand-output-section h2,
    .brand-output-section h3 {
        color: #FAFAFA;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }

    .brand-output-section h1 {
        font-size: 2rem;
        font-weight: 600;
    }
    
    .brand-output-section h2 {
        font-size: 1.5rem;
        font-weight: 600;
    }

    .brand-output-section h3 {
        font-size: 1.25rem;
        font-weight: 600;
        border-bottom: none;
    }
    
    .brand-output-section strong {
        color: #FFFFFF;
        font-weight: 600;
    }

    .brand-output-section p {
        font-size: 1rem;
        color: #E0E0E0;
        line-height: 1.6;
        word-wrap: break-word; /* Added for long string wrapping */
        overflow-wrap: break-word; /* Added for long string wrapping */
    }
    
    .brand-output-section pre {
        background-color: #1a1a1a;
        color: #E0E0E0;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #333;
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap; /* Allow code blocks to wrap */
        word-wrap: break-word;
    }
    
    .brand-output-section ul,
    .brand-output-section ol {
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
        white-space: normal; /* CHANGED: Allow text to wrap */
        word-break: break-word; /* ADDED: Force long words to break */
        border-left: 1px solid #333;
        min-width: 150px; /* ADDED: Give columns a reasonable minimum width */
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
    
    /* Fix for Streamlit's white flash on first load */
    body.stApp {
        background-color: #000000;
    }
</style>
"""

# --- 2. PAGE AND PROMPT DEFINITIONS ---

# Dictionary for page names, making it easy to change them
PAGE_NAMES = {
    "Home": "Home",
    "Branding": "Segment View",
    "MacBook": "Target Lens",
    "iPhone 16": "Market Radar",
    "Watch X": "Roadmap",
    "AirPods Max": "Pricing",
}

# --- Prompt for Segmentation (Step-by-Step) ---
PROMPT_HEADER = """
You are a Startup Market Segmentation Expert with access to generative tools and data APIs.
Your objectives:
1. Generate detailed target market and customer segmentation for the startup’s product idea.
2. Output both analytical and creative persona details, including a generated image for each persona.

Use realistic, India-specific details and current digital behavior cues.
Use INR and Asia/Kolkata context.
Avoid generic phrasing; show behavioral, digital, and cultural nuance.

Here is the startup's information:
"""

# The main prompt template
SEGMENTATION_PROMPT_TEMPLATE = """
**Startup Idea:** {idea}
**Launch Plan:** {launch_plan}
---
### Step 1: Primary Target Market
Write one crisp sentence defining:
* The broad target market (country, demographics, psychographic need).
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
* **Generated Persona Image:** [Generate and embed the image here based on the persona summary and demographics]
---
### Step 3: Segment Prioritization
* Identify 1–2 high-priority segments to target first, and justify clearly.
* Suggest the key marketing message or value proposition for them.
---
### Step 4: Positioning Implication
* Define how the brand should position itself to attract these top segments.
* Suggest tone of voice and visual style cues for creatives.
---
### Step 5: Risks / Overlooked Audiences
* Highlight blind spots, compliance or regulatory concerns (e.g., FSSAI for beverages), and emerging opportunities.
---
### Step 6: Output Formatting
Return your answer using this clean, readable structure. Use Markdown (headings, bullets) for clarity and embed generated images directly within the 'Customer Segments' section.
"""

# --- 3. HELPER FUNCTIONS ---

def inject_custom_css():
    """Injects the global CSS string into the Streamlit app."""
    st.markdown(APPLE_TAILWIND_CSS, unsafe_allow_html=True)

def create_main_navbar():
    """Creates the Apple-style pill navigation bar."""
    
    # Get the name of the current script being run
    try:
        current_page_script = st.runtime.get_script_run_ctx().page_script_hash
        current_page_name = st.session_state.page_script_hash_to_name[current_page_script]
    except Exception:
        # Fallback for initial run or if context is not available
        current_page_name = st.session_state.get("current_page", PAGE_NAMES["Home"])

    st.session_state.current_page = current_page_name
    
    # Create the navigation container
    st.markdown('<div class="apple-nav-container">', unsafe_allow_html=True)
    st.markdown('<div class="apple-nav">', unsafe_allow_html=True)
    
    # Loop through page names and create nav items
    for page_name in PAGE_NAMES.values():
        if page_name == st.session_state.current_page:
            # Selected item
            st.markdown(
                f'<a href="?page={page_name}" target="_self" class="apple-nav-item apple-nav-item-selected">{page_name}</a>', 
                unsafe_allow_html=True
            )
        else:
            # Unselected item
            st.markdown(
                f'<a href="?page={page_name}" target="_self" class="apple-nav-item">{page_name}</a>', 
                unsafe_allow_html=True
            )
            
    st.markdown('</div></div>', unsafe_allow_html=True)

def get_gemini_output(idea: str, launch_plan: str) -> str:
    """
    Generates content using the Gemini API based on the startup idea and launch plan.
    """
    try:
        # Configure the API key
        API_KEY = "AIzaSyDkoQ2M7c7EcUFpLBTMvFlAXjMg1f2TUHI"
        
        if not API_KEY:
            return "Error: GEMINI_API_KEY is not configured. Please set it in Streamlit secrets."
            
        genai.configure(api_key=API_KEY)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        
        # Construct the full prompt
        full_prompt = (
            f"{PROMPT_HEADER}\n"
            f"{SEGMENTATION_PROMPT_TEMPLATE.format(idea=idea, launch_plan=launch_plan)}"
        )
        
        # Generate content
        response = model.generate_content(full_prompt)
        
        # Extract and clean the text
        text_output = response.text
        
        # A simple regex to replace placeholder image prompts with actual placeholder images
        # This makes the output look more complete
        placeholder_url = "https://placehold.co/600x400/2a2a2a/808080?text=Persona+Image"
        cleaned_output = re.sub(
            r"\[Generate and embed the image here.*?\]",
            f"![Persona Image]({placeholder_url})",
            text_output
        )
        
        return cleaned_output

    except Exception as e:
        # st.error(f"An error occurred while calling the Gemini API: {e}")
        return f"Error: Could not generate response. Details: {str(e)}"

# --- 4. PAGE FUNCTIONS ---

def main_page():
    """The main Home page with the input form."""
    create_main_navbar()
    
    st.markdown('<h1 class="apple-hero-title">Startup Idea Accelerator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="apple-hero-subtitle">Define your idea. We\'ll help you build the brand.</p>', unsafe_allow_html=True)

    # Wrap the form in a custom container
    st.markdown('<div class="brand-form-container">', unsafe_allow_html=True)
    
    with st.form(key="brand_form"):
        # Get existing values from session state or use default placeholders
        idea = st.session_state.get("startup_idea", "")
        launch_plan = st.session_state.get("startup_launch_plan", "")

        # Text area 1: The Idea
        # Swapped: Placeholder is now the question, label is the title
        startup_idea = st.text_area(
            "What is your product or service? What makes your product unique? How will you sell it?",
            value=idea,
            placeholder="e.g., A subscription service for AI-powered coding tutors for high school students in India.",
            key="startup_idea_input"
        )
        
        # Text area 2: The Launch Plan
        # Swapped: Placeholder is now the question, label is the title
        startup_launch_plan = st.text_area(
            "Where are you launching first? Who is your ideal customer? Any constraints?",
            value=launch_plan,
            placeholder="e.g., Starting with a beta in Mumbai and Delhi, targeting parents of students in IB and CBSE schools.",
            key="startup_launch_plan_input"
        )

        # Submit Button
        submit_button = st.form_submit_button(label="Generate My Brand")

    st.markdown('</div>', unsafe_allow_html=True)
    
    if submit_button:
        # Save inputs to session state
        st.session_state.startup_idea = startup_idea
        st.session_state.startup_launch_plan = startup_launch_plan
        
        # Show a temporary spinner while generating
        with st.spinner("Analyzing your idea and building brand strategy..."):
            # Call Gemini to get the segmentation output
            # This will run in the background and the result is implicitly
            # stored for when the 'Segment View' page is loaded.
            # We call it here to "warm up" the cache if needed, or just to run.
            # A more robust way would be to store the output in session_state.
            
            segmentation_output = get_gemini_output(startup_idea, startup_launch_plan)
            st.session_state.segmentation_output = segmentation_output
        
        # Use st.success for a clear confirmation
        st.success("Your strategy is ready! Check out the 'Segment View' page.")
        
        # Automatically switch to the "Segment View" page
        st.query_params["page"] = PAGE_NAMES["Branding"]
        time.sleep(0.1) # Give streamlit time to register query param change
        st.rerun()


def page_a():
    """'Segment View' Page (formerly Branding)"""
    create_main_navbar()
    st.markdown(f'<h1 class="apple-page-title">{PAGE_NAMES["Branding"]}</h1>', unsafe_allow_html=True)
    
    # Check if idea and launch plan are in session state
    idea = st.session_state.get("startup_idea")
    launch_plan = st.session_state.get("startup_launch_plan")
    
    if not idea or not launch_plan:
        st.warning("Please fill out the form on the Home page first to generate your segmentation.")
        return

    # Check if output is already generated and cached in session state
    if "segmentation_output" in st.session_state:
        output = st.session_state.segmentation_output
    else:
        # If not, generate it now (e.g., if user bookmarks this page)
        with st.spinner("Generating segmentation analysis..."):
            output = get_gemini_output(idea, launch_plan)
            st.session_state.segmentation_output = output

    # Display the generated output in the custom container
    st.markdown('<div class="brand-output-section">', unsafe_allow_html=True)
    st.markdown(output, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_b():
    """'Target Lens' Page (formerly MacBook)"""
    create_main_navbar()
    st.markdown(f'<h1 class="apple-page-title">{PAGE_NAMES["MacBook"]}</h1>', unsafe_allow_html=True)
    st.markdown("## Power. It's in the Air.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        The new MacBook Air, supercharged by the M4 chip, brings astonishing performance and 
        all-day battery life to an impossibly thin aluminum enclosure.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**M4 Chip:** Neural Engine for advanced AI tasks.</li>
            <li>**Liquid Retina Display:** 13.6" or 15.3" with ProMotion.</li>
            <li>**New Colors:** Midnight, Starlight, Space Gray, and Silver.</li>
        </ul>
    """, unsafe_allow_html=True)

def page_c():
    """'Market Radar' Page (formerly iPhone 16)"""
    create_main_navbar()
    st.markdown(f'<h1 class="apple-page-title">{PAGE_NAMES["iPhone 16"]}</h1>', unsafe_allow_html=True)
    st.markdown("## A new era of intelligence.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        iPhone 16 Pro integrates Apple Intelligence, a new standard for personal AI. 
        The A18 Pro chip unlocks capabilities that are intuitive, powerful, and private.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**Apple Intelligence:** On-device processing for privacy.</li>
            <li>**Pro Camera System:** 48MP Main with new anti-reflective coating.</li>
            <li>**Action Button:** Now with more customizable shortcuts.</li>
        </ul>
    """, unsafe_allow_html=True)

def page_d():
    """'Roadmap' Page (formerly Watch X)"""
    create_main_navbar()
    st.markdown(f'<h1 class="apple-page-title">{PAGE_NAMES["Watch X"]}</h1>', unsafe_allow_html=True)
    st.markdown("## Redesigned. Reimagined.")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        The 10th-anniversary Apple Watch X features the thinnest-ever case, a new magnetic 
        band system, and breakthrough health monitoring.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**S10 SiP:** Faster, more efficient processing.</li>
            <li>**Blood Glucose Monitoring:** Non-invasive monitoring capability.</li>
            <li>**New Health Sensors:** Advanced crash-detection.</li>
        </ul>
    """, unsafe_allow_html=True)

    
def page_e():
    """'Pricing' Page (formerly AirPods Max)"""
    create_main_navbar()
    st.markdown(f'<h1 class="apple-page-title">{PAGE_NAMES["AirPods Max"]} (Gen 2)</h1>', unsafe_allow_html=True)
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


# --- 5. MAIN APPLICATION LOGIC ---

# Map page names to their corresponding functions
page_functions = {
    PAGE_NAMES["Home"]: main_page,
    PAGE_NAMES["Branding"]: page_a,
    PAGE_NAMES["MacBook"]: page_b,
    PAGE_NAMES["iPhone 16"]: page_c,
    PAGE_NAMES["Watch X"]: page_d,
    PAGE_NAMES["AirPods Max"]: page_e,
}

def main():
    st.set_page_config(page_title="Startup Accelerator", layout="wide")
    inject_custom_css()

    # --- Page Routing ---
    # Use URL query parameters to determine which page to show
    query_params = st.query_params
    
    if "page" in query_params:
        # Get the page name from the URL query
        page_name_from_query = query_params["page"]
        
        # Find the corresponding function
        # This is a reverse lookup from the display name to the function
        page_to_show = main_page # Default to home
        for key, display_name in PAGE_NAMES.items():
            if display_name == page_name_from_query:
                page_to_show = page_functions[display_name]
                break
    else:
        # Default to the Home page
        page_to_show = main_page

    # Run the selected page function
    page_to_show()

if __name__ == "__main__":
    main()
