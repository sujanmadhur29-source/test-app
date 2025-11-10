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
        font-size: 1.25rem;
        font-weight: 400;
        text-align: center;
        color: #888888;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .apple-page-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        border-bottom: 1px solid #333;
        padding-bottom: 1rem;
    }

    /* 3. Custom Navigation Bar */
    .apple-nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #1a1a1a;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        width: 100%;
    }
    .apple-nav-item {
        color: #a0a0a0;
        text-decoration: none;
        padding: 0.5rem 1rem;
        margin: 0 0.25rem;
        font-weight: 500;
        border-radius: 8px;
        transition: background-color 0.2s, color 0.2s;
    }
    .apple-nav-item:hover {
        color: #ffffff;
        background-color: #333333;
    }
    .apple-nav-item-active {
        color: #ffffff;
        background-color: #007aff; /* Apple Blue */
    }

    /* 4. Custom Form Elements */
    .stTextArea label, .stTextInput label {
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Make text area placeholder text smaller and italic */
    .stTextArea textarea::placeholder {
        font-size: 0.9rem;
        color: #888;
        font-style: italic;
    }

    .stButton>button {
        background-color: #007aff;
        color: #ffffff;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        border-radius: 12px;
        border: none;
        transition: background-color 0.2s;
        width: 100%; /* Make button full-width */
        margin-top: 1rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }

    /* 5. Custom Output Container */
    .brand-output-section {
        background-color: #1c1c1e;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        min-height: 200px;
        border: 1px solid #333;
    }
    
    .brand-output-section h1, .brand-output-section h2, .brand-output-section h3, .brand-output-section h4 {
        color: #f5f5f7;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #444;
        padding-bottom: 0.25rem;
    }
    
    .brand-output-section p, .brand-output-section li {
        color: #d2d2d7;
        line-height: 1.6;
        /* Add text wrapping for long strings */
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* --- CSS FOR RESPONSIVE IMAGES --- */
    .brand-output-section img {
        border-radius: 8px;
        margin-top: 1rem;
        max-width: 100%; /* Make image responsive */
        height: auto;      /* Maintain aspect ratio */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* --- CSS FOR SCROLLABLE & WRAPPING TABLES --- */
    .brand-output-section table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        display: block;
        overflow-x: auto; /* Enable horizontal scrolling */
        white-space: normal; /* Allow text wrapping */
    }
    .brand-output-section th, .brand-output-section td {
        border: 1px solid #444;
        padding: 0.75rem;
        text-align: left;
        color: #d2d2d7;
        word-break: break-word; /* Break long words */
        min-width: 120px; /* Ensure columns have a readable width */
    }
    .brand-output-section th {
        background-color: #333;
        color: #f5f5f7;
        white-space: nowrap; /* Keep headers on one line */
    }

    /* Info/Warning/Error boxes */
    .info-box {
        background-color: #2c2c2e;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: #a0a0a0;
    }
    
    .input-summary-section {
        background-color: #1c1c1e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    /* Hide default Streamlit Chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# Apply the custom CSS at the start
st.set_page_config(layout="wide")
st.markdown(APPLE_TAILWIND_CSS, unsafe_allow_html=True)

# --- 2. GEMINI API CONFIGURATION ---

# Configure the API key from Streamlit secrets
try:
    # API_KEY = st.secrets["GEMINI_API_KEY"] # Replaced secret with hardcoded key
    API_KEY = "AIzaSyDkoQ2M7c7EcUFpLBTMvFlAXjMg1f2TUHI"
    if not API_KEY:
        raise ValueError("API key is not set")
    genai.configure(api_key=API_KEY)
    # model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025") # Model will be initialized in each function
    GEMINI_ENABLED = True
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please check the API key.")
    GEMINI_ENABLED = False

# The prompt template to be filled by user inputs
SEGMENTATION_PROMPT_TEMPLATE = """
You are a Startup Market Segmentation Expert with access to generative tools and data APIs.
Your objectives:
1. Generate detailed target market and customer segmentation for the startup’s product idea.
2. Output both analytical and creative persona details, including a generated image for each persona.

---
USER INPUTS:
Startup Idea: {idea}
Launch Plan: {launch_plan}
---
Based *only* on the inputs above, generate the following:

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
Use realistic, India-specific details and current digital behavior cues.
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
---
### Constraints
* Keep it concise, practical, and realistic to the Indian market.
* Use INR and Asia/Kolkata context.
* Avoid generic phrasing; show behavioral, digital, and cultural nuance relevant to the user's idea.
"""

# --- NEW: TLPrompt (Target Lens Prompt) ---
TL_PROMPT_TEMPLATE = """
You are a Competitive Intelligence and Marketing Landscape Analyst with access to data APIs (Similarweb, Crayon, Relevance AI).
Your goal: To deliver a comprehensive, insight-driven competitor landscape report.

---
CONTEXT FROM PREVIOUS STEP (Startup Idea & Market Segments):
{segmentation_data}
---
Based *only* on the context above (startup idea, target market, personas), generate the following competitive analysis:

Step 1 | Competitor Identification
Use Similarweb, Crayon, or Relevance AI APIs to:
• Identify 5–7 direct and indirect competitors in the same product category and geography.
• Mention each brand’s focus (e.g., RTD coffee, café chain, functional beverage).
• Add URLs or handles where possible.
• If data is unavailable, infer logically and mark “(assumed).”

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
• Identify key trends and consumer behaviors using Relevance AI or Similarweb data (e.g., search interest, engagement growth).
• Summarize market trajectory (growing / maturing / fragmented).
• Highlight 3 whitespace areas where existing players underperform.

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

1.  **Market Perceptual Map:** A 2x2 matrix for the competitor landscape (e.g., axes: Price vs. Niche).
2.  **Market Share Pie Chart:** An estimated market share pie chart for the identified competitors.
3.  **Sentiment Word Clouds:** Two simple word clouds, one for Positive and one for Negative customer sentiment.
---

### Step 7: Output Formatting (Text)
Return all text output from Steps 1-5 as plain text sections:
Competitor Landscape Overview:
<paragraph>
Competitor Snapshots:
<Brand> – <summary>
…
Market & Category Insights:
<paragraph>
Deeper Digital & Creative Intelligence:
<paragraph>
Strategic Implications:
<paragraph>
Constraints
* Keep Indian market context (INR, Asia/Kolkata).
* Use realistic data and inferred logic when APIs don’t return live metrics.
* Maintain professional, insight-led tone.
* Output must be clean and ready for dashboard rendering.
"""

# --- NEW: TLPrompt2 (Focused Map Prompt) ---
TL_PROMPT_TEMPLATE_2 = """
Based on the following competitive analysis output, generate *only* a Competitor The Market Perceptual Map (or 2x2 Matrix) image. Do not give any additional text.

---
ANALYSIS CONTEXT:
{tl_text_data}
---
"""


# --- 3. STATE AND NAVIGATION FUNCTIONS ---

# Define page names and keys
PAGE_NAMES = {
    "Home": "home",
    "Segment View": "page_a",
    "Target Lens": "page_b",
    "Market Radar": "page_c",
    "Roadmap": "page_d",
    "Pricing": "page_e"
}

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = PAGE_NAMES["Home"]
if 'startup_idea' not in st.session_state:
    st.session_state.startup_idea = ""
if 'startup_launch_plan' not in st.session_state:
    st.session_state.startup_launch_plan = ""
if 'segmentation_output' not in st.session_state:
    st.session_state.segmentation_output = None
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'target_lens_output' not in st.session_state:
    st.session_state.target_lens_output = None
if 'target_lens_map_image' not in st.session_state: # NEW state for the focused map
    st.session_state.target_lens_map_image = None


def navigate_to(page_key):
    """Updates the session state to navigate to a new page."""
    st.session_state.current_page = page_key

def create_main_navbar():
    """Creates the static horizontal navigation bar."""
    st.markdown('<div class="apple-nav-container">', unsafe_allow_html=True)
    
    # Get the value (e.g., "page_a") of the current page
    current_page_value = st.session_state.current_page
    
    for page_name, page_key in PAGE_NAMES.items():
        is_active = (page_key == current_page_value)
        active_class = "apple-nav-item-active" if is_active else ""
        
        # We use a dummy query param to force Streamlit to re-run the link
        # This is a common pattern for creating custom navigation
        st.markdown(f"""
            <a href="?page={page_key}" class="apple-nav-item {active_class}" target="_self">
                {page_name}
            </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PAGE CONTENT FUNCTIONS ---

def main_page():
    """The main Home page with the input form."""
    create_main_navbar()
    
    st.markdown("""
        <div style="text-align: center;">
            <h1 class="apple-hero-title">Futurecaster</h1>
            <p class="apple-hero-subtitle">
                Turn your startup idea into a comprehensive market strategy.
                Describe your concept and launch plan to generate your strategic playbook.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key="brand_form"):
        st.text_area(
            "What idea do you have in mind?",
            key="form_startup_idea",
            value=st.session_state.startup_idea,
            placeholder="What is your product or service? What makes your product unique? How will you sell it?",
            height=150
        )
        
        st.text_area(
            "What are your thoughts on a launch plan?",
            key="form_startup_launch_plan",
            value=st.session_state.startup_launch_plan,
            placeholder="Where are you launching first? Who is your ideal customer? Any constraints?",
            height=150
        )

        submit_button = st.form_submit_button(label="Generate My Playbook")

        if submit_button:
            if not GEMINI_ENABLED:
                st.error("Generation is disabled. Please configure your Gemini API key.")
            elif not st.session_state.form_startup_idea or not st.session_state.form_startup_launch_plan:
                st.warning("Please fill out both fields to generate your playbook.")
            else:
                # Save data, set generating flag, and navigate
                st.session_state.startup_idea = st.session_state.form_startup_idea
                st.session_state.startup_launch_plan = st.session_state.form_startup_launch_plan
                st.session_state.generating = True
                
                # Clear old outputs on new submission
                st.session_state.segmentation_output = None
                st.session_state.target_lens_output = None
                st.session_state.target_lens_map_image = None # NEW: Clear focused map
                
                navigate_to(PAGE_NAMES["Segment View"]) # FIXED: Was "Branding"
                st.rerun()


# --- 4. GEMINI API CALL FUNCTION ---

def get_segmentation_output(idea, launch_plan):
    """
    Calls the Gemini API with the segmentation prompt.
    """
    if not GEMINI_ENABLED:
        return "Error: Gemini API is not configured. Please check your API key."

    # --- ADDED: Initialize text model ---
    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")

    # Format the prompt with user inputs
    prompt = SEGMENTATION_PROMPT_TEMPLATE.format(idea=idea, launch_plan=launch_plan)
    
    try:
        response = model.generate_content(prompt)
        # Clean up the output, remove Markdown backticks
        output_text = response.text.strip().replace("```markdown", "").replace("```", "")
        
        # Replace placeholder image text with actual placeholder URLs
        # This makes the page look more complete
        output_text = re.sub(
            r"\[Generate and embed the image here.*?\]",
            lambda m: f"![Persona Image](https://placehold.co/400x300/1c1c1e/d2d2d7?text=Persona+Image)",
            output_text
        )
        return output_text
    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return f"Error: Could not generate content. {e}"

# --- NEW: Target Lens Gemini Function ---
def get_target_lens_output(segmentation_data: str):
    """
    Calls the Gemini API with the Target Lens prompt, using segmentation
    data as context. Now returns both text and images.
    """
    if not GEMINI_ENABLED:
        return {"text": "Error: Gemini API is not configured.", "images": []}
        
    # --- MODEL CHANGED HERE ---
    model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
    
    # Format the prompt with the segmentation output
    prompt = TL_PROMPT_TEMPLATE.format(segmentation_data=segmentation_data)
    
    try:
        # --- GENERATION CALL CHANGED HERE ---
        generation_config = {"responseModalities": ["TEXT", "IMAGE"]}
        response = model.generate_content(prompt, generation_config=generation_config)
        
        # --- RESPONSE PROCESSING CHANGED HERE ---
        text_output = ""
        image_outputs = []
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if 'text' in part:
                    text_output += part.text + "\n"
                elif 'inlineData' in part:
                    img_data = part.inlineData
                    base64_data = img_data.data
                    mime_type = img_data.mimeType
                    image_url = f"data:{mime_type};base64,{base64_data}"
                    image_outputs.append(image_url)
                    
        return {"text": text_output.strip().replace("
