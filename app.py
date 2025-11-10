import streamlit as st
import time
import google.generativeai as genai
import os
import re # Added re for placeholder URL replacement

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
    # Use Streamlit secrets to store the API key
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    GEMINI_ENABLED = True
except Exception as e:
    # Updated error message
    st.error(f"Error configuring Gemini API: {e}. Please ensure you have a GEMINI_API_KEY in your Streamlit secrets.")
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

# --- NEW: TLPrompt (Target Lens Prompt) ---
TL_PROMPT_TEMPLATE = """
You are a Competitive Intelligence and Marketing Landscape Analyst with access to data APIs (Similarweb, Crayon, Relevance AI).
Your goal:
To deliver a comprehensive, insight-driven competitor landscape report based on the provided startup context.
---
### STARTUP CONTEXT (Input)
{segmentation_data}
---
### YOUR TASK
Based *only* on the context above (startup idea, target market, personas), generate the following competitive analysis:

Step 1 | Competitor Identification
* Identify 5–7 direct and indirect competitors in the same product category and geography.
* Mention each brand’s focus (e.g., RTD coffee, café chain, functional beverage).
* Add URLs or handles where possible.
* If data is unavailable, infer logically and mark “(assumed).”

Step 2 | Competitor Landscape Summary
For each competitor, compile:
* Brand Positioning (how they describe themselves)
* Price Tier (₹ range or value vs premium)
* Distribution Channels (retail, q-commerce, D2C, marketplaces)
* Digital Presence (traffic volume, sources, geography via Similarweb)
* Marketing Messaging (themes, tone, creative slogans from Crayon)
* Ad and Content Clusters (visual tone + sentiment using Relevance AI)
* Differentiators / Innovations (unique value props, packaging, etc.)
* **give this summary in form of a table**

Step 3 | Market & Category Insights
* Identify key trends and consumer behaviors using Relevance AI or Similarweb data (e.g., search interest, engagement growth).
* Summarize market trajectory (growing / maturing / fragmented).
* Highlight 3 whitespace areas where existing players underperform.

Step 4 | Deeper Digital & Creative Intelligence
Include if data is available:
* Comparative traffic benchmarks (top 3 competitors).
* Top traffic sources (Search / Social / Direct / Referral).
* Paid vs organic mix.
* Sentiment breakdown of top ad creatives (positive / neutral / negative).
* 3 emerging creative themes (e.g., “Clean Energy,” “Minimalist Lifestyle,” “Wellness + Craft”).

Step 5 | Strategic Implications for the Startup
Summarize:
* Key opportunities and threats from competitor scan.
* Potential differentiation levers (tone, channels, partnerships).
* Recommended price & distribution strategy.
* Early creative tone suggestion.

---
### Step 6: Generated Visuals
Based on all the analysis above, generate the following three images. Do not add any extra text, just the images.
1. **Market Perceptual Map:** A 2x2 matrix for the competitor landscape (e.g., axes: Price vs. Niche).
2. **Market Share Pie Chart:** An estimated market share pie chart for the identified competitors.
3. **Sentiment Word Clouds:** Two simple word clouds, one for Positive and one for Negative customer sentiment.

---
### Step 7: Output Formatting (Text)
Return all text output from Steps 1-5 as plain text sections:
Competitor Landscape Overview: <paragraph>
Competitor Snapshots: <Brand> – <summary>
…
Market & Category Insights: <paragraph>
Deeper Digital & Creative Intelligence: <paragraph>
Strategic Implications: <paragraph>
### Constraints
* Keep Indian market context (INR, Asia/Kolkata).
* Use realistic data and inferred logic when APIs don’t return live metrics.
* Maintain professional, insight-led tone.
* Output must be clean and ready for dashboard rendering.
"""

# --- NEW: MRPrompt1 (Market Radar Prompt) ---
# This prompt is designed to take the *output* of the previous two steps
# as its context, solving the problem of missing fields like 'Budget'.
MR_PROMPT_TEMPLATE = """
You are a Brand Positioning & Targeting Strategist with access to GenAI and audience/data tools (Relevance AI, Meta Audience Insights, Google Ads, Similarweb).

Your task:
Build a fully-formed Positioning & Targeting Strategy for the startup based on the context below.

---

### Step 1 | Available Context

This is the information I have about the startup. Use this to inform your analysis. 
Where information is missing (like a specific 'Budget'), make logical assumptions based on the context and proceed.

**User Inputs:**
{user_inputs}

**Segmentation Analysis (includes Target Segments):**
{segmentation_data}

**Competitor Analysis (includes Competitor Set):**
{target_lens_data}

---

### Step 2 | Audience Refinement (GenAI & Data)

For each target segment identified in the context above:
• Derive Audience DNA: demographics, top interests, reach/CPM, negative audiences  
• Estimate CPM/CPC, CTR, CVR (mark **ASSUMED** if no exact data)  
• Provide summary:  
  - Audience DNA paragraph  
  - Top 5 interests/keywords with source  
  - Estimated Reach, CPM (₹), CPC (₹), Channels  

Restrict at Step2 in this response. Don’t ask additional questions at the end.
"""


# --- 3. STATE AND NAVIGATION FUNCTIONS ---
PAGE_NAMES = {
    "Home": "main_page",
    "Segment View": "page_a", # Renamed
    "Target Lens": "page_b", # Renamed
    "Market Radar": "page_c", # Renamed
    "Roadmap": "page_d", # Renamed
    "Pricing": "page_e", # Renamed
}

# Initialize session state for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]

# --- State for Form Inputs ---
if 'startup_idea' not in st.session_state:
    st.session_state.startup_idea = None
if 'startup_launch_plan' not in st.session_state:
    st.session_state.startup_launch_plan = None
if 'generating' not in st.session_state:
    st.session_state.generating = False

# --- NEW: Session state for generated outputs ---
if 'segmentation_output' not in st.session_state:
    st.session_state.segmentation_output = None
if 'target_lens_output' not in st.session_state:
    st.session_state.target_lens_output = None
# --- NEW: State for Market Radar ---
if 'market_radar_output' not in st.session_state:
    st.session_state.market_radar_output = None


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
        if st.button(page_keys[1], key="nav_seg", disabled=is_active):
            navigate_to(page_values[1])
            st.rerun()

    with cols[2]:
        is_active = st.session_state.current_page == page_values[2]
        if st.button(page_keys[2], key="nav_lens", disabled=is_active):
            navigate_to(page_values[2])
            st.rerun()

    with cols[3]:
        is_active = st.session_state.current_page == page_values[3]
        if st.button(page_keys[3], key="nav_radar", disabled=is_active):
            navigate_to(page_values[3])
            st.rerun()

    with cols[4]:
        is_active = st.session_state.current_page == page_values[4]
        if st.button(page_keys[4], key="nav_road", disabled=is_active):
            navigate_to(page_values[4])
            st.rerun()
            
    with cols[5]:
        is_active = st.session_state.current_page == page_values[5]
        if st.button(page_keys[5], key="nav_price", disabled=is_active):
            navigate_to(page_values[5])
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# --- 4. GEMINI API CALL FUNCTIONS ---

def get_segmentation_output(idea, launch_plan):
    """
    Generates content using the SEGMENTATION_PROMPT_TEMPLATE.
    """
    if not GEMINI_ENABLED:
        return "Gemini API is not configured."

    try:
        # Use a reliable, current model
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        # Format the prompt
        prompt = SEGMENTATION_PROMPT_TEMPLATE.format(
            idea=idea,
            launch_plan=launch_plan
        )
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Clean the response text, remove common markdown "ticks"
        cleaned_text = response.text.strip().lstrip("```markdown").rstrim("```").strip()
        
        # Replace placeholder image URLs to ensure they are valid
        # E.g., ...[Persona Name](https://placehold.co/...)
        cleaned_text = re.sub(
            r'\[(.*?)\]\((https:\/\/placehold\.co\/.*?)\)',
            r'![Persona Image](\2)',
            cleaned_text
        )
        # E.g., Just a raw URL https://placehold.co/...
        cleaned_text = re.sub(
            r'https://placehold\.co/300x300/E0E0E0/000000\?text=([\w+\-]+)',
            r'https://placehold.co/300x300/E0E0E0/000000?text=\1',
            cleaned_text
        )

        return cleaned_text
    
    except Exception as e:
        st.error(f"Error calling Gemini API (Segmentation): {e}")
        return None

def get_target_lens_output():
    """
    Generates content using the TL_PROMPT_TEMPLATE.
    This function *depends on* segmentation_output.
    """
    if not GEMINI_ENABLED:
        return "Gemini API is not configured."
        
    if not st.session_state.segmentation_output:
        st.warning("Segmentation data is missing. Cannot generate Target Lens.")
        return None

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        # Format the prompt
        prompt = TL_PROMPT_TEMPLATE.format(
            segmentation_data=st.session_state.segmentation_output
        )
        
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip("```markdown").rstrim("```").strip()
        
        return cleaned_text
    
    except Exception as e:
        st.error(f"Error calling Gemini API (Target Lens): {e}")
        return None

# --- NEW: Market Radar Function ---
def get_market_radar_output():
    """
    Generates content using the MR_PROMPT_TEMPLATE.
    This function *depends on* segmentation_output and target_lens_output.
    """
    if not GEMINI_ENABLED:
        return "Gemini API is not configured."
        
    if not st.session_state.segmentation_output or not st.session_state.target_lens_output:
        st.warning("Prerequisite data is missing. Cannot generate Market Radar.")
        return None

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        # Create a simple summary of the user inputs
        user_inputs_str = f"""
* **Startup Idea:** {st.session_state.startup_idea}
* **Launch Plan:** {st.session_state.startup_launch_plan}
"""
        
        # Format the prompt
        prompt = MR_PROMPT_TEMPLATE.format(
            user_inputs=user_inputs_str,
            segmentation_data=st.session_state.segmentation_output,
            target_lens_data=st.session_state.target_lens_output
        )
        
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip("```markdown").rstrim("```").strip()
        
        return cleaned_text
    
    except Exception as e:
        st.error(f"Error calling Gemini API (Market Radar): {e}")
        return None


def on_generate_click():
    """
    Callback function for the 'Generate' button.
    Stores inputs, sets generating flag, and fetches all outputs.
    """
    # 1. Store inputs in session state
    st.session_state.startup_idea = st.session_state.temp_idea
    st.session_state.startup_launch_plan = st.session_state.temp_launch_plan
    st.session_state.generating = True
    
    # 2. Clear all previous outputs
    st.session_state.segmentation_output = None
    st.session_state.target_lens_output = None
    st.session_state.market_radar_output = None

    try:
        # --- Step 1: Get Segmentation ---
        with st.spinner("Generating... (Step 1/3: Segmentation)"):
            seg_output = get_segmentation_output(
                st.session_state.startup_idea,
                st.session_state.startup_launch_plan
            )
        
        if seg_output:
            st.session_state.segmentation_output = seg_output
        else:
            raise Exception("Failed to generate segmentation output.")

        # --- Step 2: Get Target Lens ---
        with st.spinner("Generating... (Step 2/3: Target Lens)"):
            lens_output = get_target_lens_output() # Depends on state
        
        if lens_output:
            st.session_state.target_lens_output = lens_output
        else:
            raise Exception("Failed to generate target lens output.")

        # --- Step 3: Get Market Radar ---
        with st.spinner("Generating... (Step 3/3: Market Radar)"):
            radar_output = get_market_radar_output() # Depends on state
        
        if radar_output:
            st.session_state.market_radar_output = radar_output
        else:
            raise Exception("Failed to generate market radar output.")

        # If all successful, navigate to the first results page
        st.session_state.generating = False
        navigate_to(PAGE_NAMES["Segment View"])
        st.rerun()

    except Exception as e:
        st.session_state.generating = False
        st.error(f"An error occurred during generation: {e}")
        # Don't rerun, stay on page to show error

# --- 5. PAGE DEFINITIONS ---

def main_page():
    """The main 'Home' page with the input form."""
    create_main_navbar()
    
    st.markdown('<h1 class="apple-hero-title">BrandGen Studio</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="apple-hero-subtitle">Define your startup idea. We build the brand strategy.</p>',
        unsafe_allow_html=True
    )

    # Use columns for a centered, narrower form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form(key="brand_form"):
            st.text_input(
                "Your Startup Idea",
                key="temp_idea",
                placeholder="E.g., A new brand of RTD craft coffee for WFH professionals in India.",
                value=st.session_state.startup_idea or "" # Persist value
            )
            
            st.text_area(
                "Your Launch Plan & Context",
                key="temp_launch_plan",
                placeholder="E.g., Launching D2C in Mumbai & Bangalore. Target audience is 25-40. Price is premium (Rs. 150-200 per bottle). Focus on 'clean energy' and 'no preservatives'.",
                value=st.session_state.startup_launch_plan or "" # Persist value
            )

            # Use st.form_submit_button and place it in a custom container
            st.markdown('<div class="apple-primary-button-container">', unsafe_allow_html=True)
            submit_button = st.form_submit_button(
                label="Generate Strategy",
                disabled=st.session_state.generating,
                use_container_width=True # Make button full-width in this column
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if submit_button:
                if not st.session_state.temp_idea or not st.session_state.temp_launch_plan:
                    st.warning("Please fill out both fields to generate your strategy.")
                else:
                    on_generate_click()


def page_a():
    """Segment View Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Segment View</h1>', unsafe_allow_html=True)

    if st.session_state.segmentation_output:
        # Display the input summary
        st.markdown('<div class="input-summary-section">', unsafe_allow_html=True)
        st.markdown(f"<h3>Startup Idea</h3><p>{st.session_state.startup_idea}</p>", unsafe_allow_html=True)
        st.markdown(f"<h3>Launch Plan</h3><p>{st.session_state.startup_launch_plan}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the generated output
        st.markdown('<div class="brand-output-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.segmentation_output, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Please generate a strategy on the 'Home' page to see your Segment View.")

def page_b():
    """Target Lens Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Target Lens</h1>', unsafe_allow_html=True)

    if st.session_state.target_lens_output:
        # Display the input summary
        st.markdown('<div class="input-summary-section">', unsafe_allow_html=True)
        st.markdown(f"<h3>Startup Idea</h3><p>{st.session_state.startup_idea}</p>", unsafe_allow_html=True)
        st.markdown(f"<h3>Launch Plan</h3><p>{st.session_state.startup_launch_plan}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the generated output
        st.markdown('<div class="brand-output-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.target_lens_output, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Please generate a strategy on the 'Home' page to see your Target Lens.")


# --- UPDATED: Market Radar Page ---
def page_c():
    """Market Radar Page"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Market Radar</h1>', unsafe_allow_html=True)

    if st.session_state.market_radar_output:
        # Display the input summary
        st.markdown('<div class="input-summary-section">', unsafe_allow_html=True)
        st.markdown(f"<h3>Startup Idea</h3><p>{st.session_state.startup_idea}</p>", unsafe_allow_html=True)
        st.markdown(f"<h3>Launch Plan</h3><p>{st.session_state.startup_launch_plan}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the generated output
        st.markdown('<div class="brand-output-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.market_radar_output, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Please generate a strategy on the 'Home' page to see your Market Radar.")


def page_d():
    """Roadmap Page (Static)"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Roadmap</h1>', unsafe_allow_html=True)
    st.markdown("## Coming Soon: The Future of Health")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        This section will soon feature a generative roadmap based on your product, 
        highlighting key technological and market milestones.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**Q1 2026:** AI-Powered Persona Deep-Dives</li>
            <li>**Q2 2026:** Real-time Market Trend Integration</li>
            <li>**Q3 2026:** Automated GTM Creative Briefs</li>
        </ul>
    """, unsafe_allow_html=True)

def page_e():
    """Pricing Page (Static)"""
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Pricing</h1>', unsafe_allow_html=True)
    st.markdown("## Simple, Powerful Plans")
    st.markdown("""
        <p style="font-size: 1.1rem; color: #E0E0E0;">
        Currently in beta, BrandGen Studio is free to use. 
        Future plans will be based on usage and advanced features.
        </p>
        <ul style="color: #E0E0E0; list-style-type: disc; margin-left: 20px; padding-left: 0;">
            <li>**Beta (Current):** Free access</li>
            <li>**Pro (Coming Soon):** For startups needing advanced analytics</li>
            <li>**Enterprise (Coming Soon):** For agencies and VCs</li>
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

# Get the function corresponding to the current page and call it
current_page_function = page_functions.get(st.session_state.current_page, main_page)
current_page_function()
