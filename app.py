import streamlit as st
import time
import google.generativeai as genai
import os
import re
import base64  # For logo encoding

# --- NEW: Function to encode logo ---
def get_image_as_base64(file_path):
    """Reads an image file and returns it as a base64 encoded data URI."""
    try:
        with open(file_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    except FileNotFoundError:
        st.error(f"Logo file '{file_path}' not found. Please ensure 'StartWiseLogo.jpeg' is in the same directory as 'app.py'.")
        return ""  # Return empty string on error

# Get the base64 string for the logo
LOGO_FILE = "StartWiseLogo.jpeg"
logo_base64 = get_image_as_base64(LOGO_FILE)

# --- 1. CONFIGURATION AND STYLING (MIMICKING APPLE/TAILWIND) ---

APPLE_TAILWIND_CSS = """
<style>
    /* 1. Global Setup (Dark Mode and Font) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000;
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
        text-align: left; 
        margin-bottom: 0;
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
    
    /* Hero container with logo */
    .apple-hero-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .apple-hero-container img {
        width: 90px;
        height: 90px;
        border-radius: 12px; 
        flex-shrink: 0;
    }

    .apple-page-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* 3. Card/Navigation Styling */
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
    
    /* 4. Default Button Styling */
    div.stButton > button {
        background-color: #1a1a1a; 
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 9999px;
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
    
    /* 5. Horizontal Navigation Bar */
    .apple-nav-container {
        width: 100%;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 3rem;
        padding: 0.5rem 0;
        background-color: #101010;
        border-radius: 12px;
    }
    
    .apple-nav-container [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        color: #888888 !important;
        padding: 5px 10px !important;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
        width: 100%;
    }

    .apple-nav-container [data-testid="stButton"] > button:hover {
        color: #FFFFFF !important;
        background: none !important;
        border: none !important;
    }
    
    .apple-nav-container [data-testid="stButton"] > button:disabled {
        font-weight: 600;
        color: #FFFFFF !important;
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
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stTextArea"] > div > div > textarea {
        min-height: 100px;
    }

    [data-testid="stTextInput"] > div > div > input::placeholder,
    [data-testid="stTextArea"] > div > div > textarea::placeholder {
        color: #777777;
        font-size: 0.9rem;
        font-style: italic;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label {
        color: #AAAAAA;
        font-weight: 500;
        padding-bottom: 5px;
        font-size: 1.3rem !important;
    }

    /* 7. Primary Button */
    .apple-primary-button-container div.stButton > button {
        background-color: #007AFF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9999px;
        padding: 12px 28px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: background-color 0.2s;
        width: auto;
        margin-top: 1.5rem;
    }
    
    .apple-primary-button-container div.stButton > button:disabled {
        background: #333 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    .apple-primary-button-container div.stButton > button:hover {
        background-color: #0056b3 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    /* 8. Input Summary Styling */
    .input-summary-section {
        background-color: #101010;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .input-summary-section h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #AAAAAA;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .input-summary-section p {
        font-size: 1.1rem;
        color: #E0E0E0;
        line-height: 1.6;
        font-style: italic;
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
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .brand-output-section pre {
        white-space: pre-wrap;
        word-wrap: break-word;
        background-color: #080808;
        padding: 1.5rem;
        border-radius: 8px;
        color: #E0E0E0;
        font-family: 'Menlo', 'Consolas', monospace;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
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
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* Images in markdown (kept for persona placeholders) */
    .brand-output-section img {
        border-radius: 8px;
        margin-top: 1rem;
        max-width: 300px;
        border: 1px solid #333;
    }

    /* Tables: wrap, fixed layout + horizontal scroll */
    .brand-output-section table {
        display: block;
        width: 100%;
        overflow-x: auto;
        border-collapse: collapse;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #333;
        border-radius: 8px;
        table-layout: fixed;
    }

    .brand-output-section th,
    .brand-output-section td {
        border-bottom: 1px solid #333;
        padding: 0.75rem 1rem;
        color: #E0E0E0;
        white-space: normal !important;
        overflow-wrap: anywhere;
        vertical-align: top;
        border-left: 1px solid #333;
    }

    .brand-output-section th:first-child,
    .brand-output-section td:first-child {
        min-width: 180px; /* keeps “Segment Name” from squeezing */
    }

    .brand-output-section th {
        background-color: #2a2a2a;
        font-weight: 600;
        text-align: left;
    }
    
    .brand-output-section tr:first-child th:first-child {
        border-top-left-radius: 7px;
    }
    .brand-output-section tr:first-child th:last-child {
        border-top-right-radius: 7px;
    }

    /* Horizontal scroll container for wide content blocks */
    .table-scroll {
        overflow-x: auto;
        overflow-y: hidden;
        width: 100%;
        padding-bottom: 8px;
    }

    .table-scroll::-webkit-scrollbar { height: 8px; }
    .table-scroll::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
    .table-scroll::-webkit-scrollbar-track { background: #1a1a1a; }

    /* Hide default Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# --- Logo Button Style ---
LOGO_BUTTON_STYLE = f"""
<style>
    .apple-nav-container [data-testid="stColumn"]:first-child [data-testid="stButton"] > button {{
        background-image: url("{logo_base64}");
        background-size: contain; 
        background-repeat: no-repeat;
        background-position: center;
        color: transparent !important;
        width: 100%;
        height: 40px;
        border: none !important;
        background-color: #2a2a2a !important; 
        padding: 0 !important;
    }}
    .apple-nav-container [data-testid="stColumn"]:first-child [data-testid="stButton"] > button:hover {{
        background-color: #333333 !important;
        opacity: 0.8;
        color: transparent !important;
        border: none !important;
    }}
    .apple-nav-container [data-testid="stColumn"]:first-child [data-testid="stButton"] > button:disabled {{
        background-color: #2a2a2a !important;
        opacity: 1.0;
        color: transparent !important;
        border: none !important;
        cursor: default !important;
    }}
</style>
"""

# Apply the custom CSS at the start
st.set_page_config(layout="wide", page_title="Brand Generator App")
st.markdown(APPLE_TAILWIND_CSS, unsafe_allow_html=True)
if logo_base64:
    st.markdown(LOGO_BUTTON_STYLE, unsafe_allow_html=True)

# --- 2. GEMINI API CONFIGURATION ---

try:
    API_KEY = "AIzaSyCxm2tU8ule38Sc-qrBKAMc6pDSaRTsHh0"
    genai.configure(api_key=API_KEY)
    GEMINI_ENABLED = True
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please check the API key.")
    GEMINI_ENABLED = False

# ------------------ PROMPTS ------------------

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
* Identify key trends and consumer behaviors using Relevance AI or Similarweb data.
* Summarize market trajectory (growing / maturing / fragmented).
* Highlight 3 whitespace areas where existing players underperform.

Step 4 | Deeper Digital & Creative Intelligence
Include if data is available:
* Comparative traffic benchmarks (top 3 competitors).
* Top traffic sources (Search / Social / Direct / Referral).
* Paid vs organic mix.
* Sentiment breakdown of top ad creatives (positive / neutral / negative).
* 3 emerging creative themes.

Step 5 | Strategic Implications for the Startup
Summarize:
* Key opportunities and threats from competitor scan.
* Potential differentiation levers (tone, channels, partnerships).
* Recommended price & distribution strategy.
* Early creative tone suggestion.

### Output
Return only Steps 1–5 as clean markdown (no images).
"""

MR_PROMPT_TEMPLATE = """
You are a Brand Positioning & Targeting Strategist with access to GenAI and audience/data tools (Relevance AI, Meta Audience Insights, Google Ads, Similarweb).

Your task:
Build a fully-formed Positioning & Targeting Strategy for the startup below.

---
### Step 1 | Input Recap
Summarize: Product context, Geography, Model, Budget, Top segments, Competitor set, Category drivers.

---
### Step 2 | Audience Refinement (GenAI & Data)
For each target segment:
• Audience DNA (demographics, top interests, negatives)
• Estimated CPM/CPC, CTR, CVR (**ASSUMED** if no exact data)
• Summary with top 5 interests/keywords and indicative Reach & CPM (₹)

Restrict output to Step 2 only in this response.
"""

# --- 3. STATE AND NAVIGATION FUNCTIONS ---

PAGE_NAMES = {
    "Home": "main_page",
    "Segment View": "page_a",
    "Target Lens": "page_b",
    "Market Radar": "page_c",
    "Roadmap": "page_d",
    "Pricing": "page_e",
}

if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]
if 'startup_idea' not in st.session_state:
    st.session_state.startup_idea = None
if 'startup_launch_plan' not in st.session_state:
    st.session_state.startup_launch_plan = None
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'segmentation_output' not in st.session_state:
    st.session_state.segmentation_output = None
if 'target_lens_output' not in st.session_state:
    st.session_state.target_lens_output = None  # now TEXT (str)
if 'market_radar_output' not in st.session_state:
    st.session_state.market_radar_output = None

def navigate_to(page_key):
    st.session_state.current_page = page_key

def create_main_navbar():
    st.markdown('<div class="apple-nav-container">', unsafe_allow_html=True)
    cols = st.columns([1, 2, 2, 2, 2, 2])
    page_keys = list(PAGE_NAMES.keys())
    page_values = list(PAGE_NAMES.values())
    
    with cols[0]:
        is_active = st.session_state.current_page == page_values[0]
        if st.button(page_keys[0], key="nav_home", disabled=is_active):
            navigate_to(page_values[0]); st.rerun()
    with cols[1]:
        is_active = st.session_state.current_page == page_values[1]
        if st.button(page_keys[1], key="nav_branding", disabled=is_active):
            navigate_to(page_values[1]); st.rerun()
    with cols[2]:
        is_active = st.session_state.current_page == page_values[2]
        if st.button(page_keys[2], key="nav_mac", disabled=is_active):
            navigate_to(page_values[2]); st.rerun()
    with cols[3]:
        is_active = st.session_state.current_page == page_values[3]
        if st.button(page_keys[3], key="nav_iphone", disabled=is_active):
            navigate_to(page_values[3]); st.rerun()
    with cols[4]:
        is_active = st.session_state.current_page == page_values[4]
        if st.button(page_keys[4], key="nav_watch", disabled=is_active):
            navigate_to(page_values[4]); st.rerun()
    with cols[5]:
        is_active = st.session_state.current_page == page_values[5]
        if st.button(page_keys[5], key="nav_airpods", disabled=is_active):
            navigate_to(page_values[5]); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. GEMINI CALLS (TEXT-ONLY MODELS) ---

def get_segmentation_output(idea, launch_plan):
    if not GEMINI_ENABLED:
        return "Error: Gemini API is not configured. Please check your API key."

    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    prompt = SEGMENTATION_PROMPT_TEMPLATE.format(idea=idea, launch_plan=launch_plan)

    try:
        response = model.generate_content(prompt)
        text = response.text or ""

        # Convert: "Generated Persona Image: <URL>" -> Markdown image (for placeholder URLs)
        text = re.sub(
            r"Generated Persona Image\s*:\s*(https?://\S+)",
            r"![](\1)",
            text,
            flags=re.IGNORECASE
        )
        # Convert raw placehold.co URLs on standalone lines → image
        text = re.sub(
            r"^(https?://placehold\.co/\S+)$",
            r"![](\1)",
            text,
            flags=re.MULTILINE | re.IGNORECASE
        )
        # Replace instruction blocks, if any, with a safe placeholder
        fallback = "https://placehold.co/300x300/E0E0E0/000000?text=Persona"
        text = re.sub(
            r"\[Generate.*?image.*?\]",
            f"![]({fallback})",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )
        return text

    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return f"Error: Could not generate content. {e}"

def get_target_lens_output(segmentation_data: str) -> str:
    """
    TEXT-ONLY competitive analysis to avoid image model quotas.
    Returns plain markdown text.
    """
    if not GEMINI_ENABLED:
        return "Error: Gemini API is not configured. Please check your API key."

    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    prompt = TL_PROMPT_TEMPLATE.format(segmentation_data=segmentation_data)

    try:
        response = model.generate_content(prompt)
        return response.text or ""
    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return "Error: Could not generate Target Lens content."

def get_market_radar_output(segmentation_data: str) -> str:
    if not GEMINI_ENABLED:
        return "Error: Gemini API is not configured. Please check your API key."

    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    prompt = MR_PROMPT_TEMPLATE.format(segmentation_data=segmentation_data)
    try:
        response = model.generate_content(prompt)
        return response.text or ""
    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API for Market Radar: {e}")
        return "Error: Could not generate Market Radar content."

# --- 5. PAGE CONTENT FUNCTIONS ---

def main_page():
    create_main_navbar()
    logo_html = f'<img src="{logo_base64}" alt="StartWise Logo">' if logo_base64 else ""
    st.markdown(f"""
    <div class="apple-hero-container">
        {logo_html}
        <div class="apple-hero-title">Build smarter, launch faster.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p class="apple-hero-subtitle">Tell us what your brand stands for, and we’ll do the rest.</p>',
        unsafe_allow_html=True
    )
    
    with st.form(key="brand_form"):
        idea = st.text_area(
            "What idea do you have in mind?", 
            placeholder="What is your product or service? What makes your product unique? How will you sell it?",
            height=100
        )
        launch_plan = st.text_area(
            "What are your thoughts on a launch plan?", 
            placeholder="Where are you launching first? Who is your ideal customer? Any constraints?",
            height=100
        )
        st.markdown('<div class="apple-primary-button-container" style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Brand Identity", type="primary", disabled=not GEMINI_ENABLED)
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not idea or not launch_plan:
                st.error("Please fill out both fields to generate your brand identity.")
            else:
                st.session_state.startup_idea = idea
                st.session_state.startup_launch_plan = launch_plan
                st.session_state.generating = True
                st.session_state.segmentation_output = None
                st.session_state.target_lens_output = None
                st.session_state.market_radar_output = None
                navigate_to(PAGE_NAMES["Segment View"])
                st.rerun()

def page_a():
    create_main_navbar()
    if st.session_state.startup_idea and st.session_state.startup_launch_plan:
        st.markdown('<h1 class="apple-page-title">Segment View</h1>', unsafe_allow_html=True)
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
            with st.spinner("Generating Brand Strategy (3 steps)..."):
                st.write("Step 1/3: Generating Market Segmentation...")
                segmentation_output = get_segmentation_output(
                    st.session_state.startup_idea, 
                    st.session_state.startup_launch_plan
                )
                st.session_state.segmentation_output = segmentation_output

                if segmentation_output and not segmentation_output.startswith("Error:"):
                    st.write("Step 2/3: Generating Competitive Analysis...")
                    target_lens_output = get_target_lens_output(segmentation_output)
                    st.session_state.target_lens_output = target_lens_output

                    st.write("Step 3/3: Generating Positioning Strategy...")
                    market_radar_output = get_market_radar_output(segmentation_output)
                    st.session_state.market_radar_output = market_radar_output

                    st.write("Generation complete!")
                else:
                    st.error("Error during Step 1: Segmentation. Halting generation.")
                    st.session_state.target_lens_output = "Error: Could not generate Target Lens data because Segmentation failed."
                    st.session_state.market_radar_output = "Error: Could not generate Market Radar data because Segmentation failed."

                st.session_state.generating = False
        
        if st.session_state.segmentation_output:
            output_placeholder.markdown(
                f'''
                <div class="brand-output-section">
                    <div class="table-scroll">
                        {st.session_state.segmentation_output}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        elif not st.session_state.generating:
            output_placeholder.error("There was an issue generating the segmentation output.")
    else:
        st.markdown('<h1 class="apple-page-title">Segment View</h1>', unsafe_allow_html=True)
        st.markdown("## Define Your Identity.")
        st.markdown("""
            <p style="font-size: 1.1rem; color: #AAAAAA; margin-top: 2rem;">
            <i>To generate a brand identity, please return to the <b>Home</b> page and fill out the form.</i>
            </p>
        """, unsafe_allow_html=True)

def page_b():
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Target Lens</h1>', unsafe_allow_html=True)
    if st.session_state.startup_idea and st.session_state.startup_launch_plan:
        st.markdown(f"""
        <div class="input-summary-section">
            <h3>Startup Idea</h3>
            <p>"{st.session_state.startup_idea}"</p>
            <h3 style="margin-top: 1rem;">Launch Plan</h3>
            <p>"{st.session_state.startup_launch_plan}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        output_placeholder = st.empty()

        if st.session_state.target_lens_output:
            output_placeholder.markdown(
                f'''
                <div class="brand-output-section">
                    <div class="table-scroll">
                        {st.session_state.target_lens_output}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        elif st.session_state.generating:
            output_placeholder.info("Your analysis is being generated. Please wait...")
        else:
            output_placeholder.warning("Could not find generated analysis. Please try submitting the form again from the Home page.")
    else:
        st.markdown("## Analyze Your Competition.")
        st.markdown("""
            <p style="font-size: 1.1rem; color: #AAAAAA; margin-top: 2rem;">
            <i>To generate a competitive analysis, please return to the <b>Home</b> page and fill out the form.</i>
            </p>
        """, unsafe_allow_html=True)

def page_c():
    create_main_navbar()
    st.markdown('<h1 class="apple-page-title">Market Radar</h1>', unsafe_allow_html=True)
    if st.session_state.startup_idea and st.session_state.startup_launch_plan:
        st.markdown(f"""
        <div class="input-summary-section">
            <h3>Startup Idea</h3>
            <p>"{st.session_state.startup_idea}"</p>
            <h3 style="margin-top: 1rem;">Launch Plan</h3>
            <p>"{st.session_state.startup_launch_plan}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        output_placeholder = st.empty()
        if st.session_state.market_radar_output:
            output_placeholder.markdown(
                f'<div class="brand-output-section">{st.session_state.market_radar_output}</div>', 
                unsafe_allow_html=True
            )
        elif st.session_state.generating:
            output_placeholder.info("Your analysis is being generated. Please wait...")
        else:
            output_placeholder.warning("Could not find generated analysis. Please try submitting the form again from the Home page.")
    else:
        st.markdown("## Define Your Positioning.")
        st.markdown("""
            <p style="font-size: 1.1rem; color: #AAAAAA; margin-top: 2rem;">
            <i>To generate a positioning and targeting strategy, please return to the <b>Home</b> page and fill out the form.</i>
            </p>
        """, unsafe_allow_html=True)

def page_d():
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
    PAGE_NAMES["Segment View"]: page_a,
    PAGE_NAMES["Target Lens"]: page_b,
    PAGE_NAMES["Market Radar"]: page_c,
    PAGE_NAMES["Roadmap"]: page_d,
    PAGE_NAMES["Pricing"]: page_e,
}

page_functions[st.session_state.current_page]()
