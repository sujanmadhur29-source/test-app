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
    }

    .brand-output-section img {
        border-radius: 8px;
        margin-top: 1rem;
        max-width: 300px;
        border: 1px solid #333;
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
        submitted = st.form_submit_button("Generate Brand Identity", type="primary")
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


# --- Mock Generation and Prompt Template ---

def get_mock_segmentation_output(idea, launch_plan):
    """
    Simulates a call to the Gemini API based on the new segmentation prompt.
    This is now a "smarter" mock that dynamically builds the output
    based on keywords in the inputs.
    """
    
    # --- 1. Parse Inputs for Dynamic Insertion ---
    
    # Simple product name (e.g., "CodeTutor" from "A subscription service for AI-powered coding tutors")
    product_name = "Your Product"
    if idea and len(idea.split(' ')) > 0:
        # Try to find a noun phrase
        if "service for" in idea.lower():
            product_name = idea.lower().split("service for")[-1].strip().capitalize()
        elif "app for" in idea.lower():
            product_name = idea.lower().split("app for")[-1].strip().capitalize()
        else:
            product_name = idea.split(' ')[0].capitalize()
            if product_name.lower() in ['a', 'an', 'the'] and len(idea.split(' ')) > 1:
                 product_name = idea.split(' ')[1].capitalize()
    
    # Simple launch city parsing
    launch_city = "Bangalore" # Default
    if "mumbai" in launch_plan.lower():
        launch_city = "Mumbai"
    elif "delhi" in launch_plan.lower():
        launch_city = "Delhi"
    elif "pune" in launch_plan.lower():
        launch_city = "Pune"
    elif "chennai" in launch_plan.lower():
        launch_city = "Chennai"

    # Simple ideal customer parsing
    ideal_customer = "tech professionals" # Default
    if "student" in launch_plan.lower():
        ideal_customer = "students"
    elif "startup" in launch_plan.lower():
        ideal_customer = "tech startups"
    elif "doctor" in launch_plan.lower() or "medical" in launch_plan.lower():
        ideal_customer = "doctors"
    elif "home cook" in launch_plan.lower() or "food" in idea.lower():
        ideal_customer = "home cooks"
    elif "teacher" in launch_plan.lower() or "education" in idea.lower():
        ideal_customer = "teachers"
        
    # Use placeholder images
    img1_url = f"https://placehold.co/300x300/E0E0E0/000000?text=Persona+1+({ideal_customer})"
    img2_url = f"https://placehold.co/300x300/B0B0B0/000000?text=Persona+2+({launch_city})"

    
    # --- 2. Dynamically build the mock output string section by section ---
    
    # --- Step 1 ---
    step1 = f"""
### Step 1: Primary Target Market
The primary target market is **{ideal_customer}** in urban India (initially **{launch_city}**), aged 18-35, who are actively seeking a solution for: *{idea[:60]}...*
"""
    
    # --- Step 2 (Dynamic Personas) ---
    
    # Create persona templates
    persona1_name = "Segment 1: The 'Core User'"
    persona1_demo = f"23-30, Any Gender, Mid-income, Tier 1 city ({launch_city})."
    persona1_psych = "Digitally native, values convenience and efficiency, willing to pay for quality."
    persona1_pain = f"Struggles with the 'old way' of doing things. Specifically, needs help with **{product_name}**."
    persona1_summary = f"This user is a busy professional in {launch_city} who fits your target of **{ideal_customer}**. They are frustrated with current solutions for *{idea[:40]}...* and are actively searching for a better tool like **{product_name}**."

    persona2_name = "Segment 2: The 'Explorer'"
    persona2_demo = "18-24, Any Gender, Low-income (student/early-career), Tier 1/2 cities."
    persona2_psych = "Curious, loves trying new tech, price-sensitive, highly social and vocal."
    persona2_pain = f"Wants to learn about or try *{idea[:40]}...* but finds existing options too expensive or complex."
    persona2_summary = f"This user is a student or new graduate in {launch_city} who is excited by new technology. They might not be a paying user today, but they are your future evangelist and will spread the word about **{product_name}** in their social circles."

    # Overwrite with specific templates if keywords match
    if ideal_customer == "students":
        persona1_name = "Aarav K. (The Ambitious Student)"
        persona1_demo = f"18-22, Male/Female, Low-income (student), Tier 1/2 city (e.g., {launch_city}, Pune)."
        persona1_psych = "Stressed about placements, values academic performance, FOMO, digitally native."
        persona1_pain = f"Needs a better way to learn than the college curriculum. Specifically, needs help with **{product_name}**."
        persona1_summary = f"Aarav is a 3rd-year B.Tech student in {launch_city} juggling assignments. He's stressed about placements and feels his college syllabus is outdated. He needs a tool like **{product_name}** to explain complex concepts at 2 AM."

        persona2_name = "Priya S. (The Early-Career Accelerator)"
        persona2_demo = f"23-28, Male/Female, Income ₹8L-₹15L, Tier 1 city ({launch_city}, Mumbai)."
        persona2_psych = "Career-focused, time-poor, values efficiency and ROI, invests in self-improvement."
        persona2_pain = f"Lacks time for long courses, needs specific, on-the-job answers related to **{product_name}**."
        persona2_summary = f"Priya is a Software Engineer with 2 years of experience at a {launch_city} startup. She wants to get promoted and sees **{product_name}** as a key tool to help her. She's frustrated by generic solutions and needs something that solves her specific problem: *{idea[:30]}...*"

    elif ideal_customer == "doctors":
        persona1_name = "Dr. Rohan M. (The Resident)"
        persona1_demo = f"26-32, Male/Female, Stipend/Early Salary, Metros ({launch_city})."
        persona1_psych = "Overworked, time-poor, values accuracy and speed, evidence-based."
        persona1_pain = f"Struggles with administrative overhead, needs a faster way to access patient info or diagnostics. Your idea, **{product_name}**, could help."
        persona1_summary = f"Rohan is a resident at a top {launch_city} hospital. He's on his feet 18 hours a day. He needs a tool like **{product_name}** to quickly manage *{idea[:30]}...* between rounds, rather than using outdated hospital software."
        
        persona2_name = "Dr. Ananya V. (The Specialist)"
        persona2_demo = f"35-45, Female, High Income, Tier 1 ({launch_city}, Mumbai, Delhi)."
        persona2_psych = "Runs a private practice, values patient experience, wants to optimize her clinic."
        persona2_pain = f"Managing appointments and patient follow-ups is chaotic. **{product_name}** could streamline her practice."
        persona2_summary = f"Ananya is a specialist in {launch_city} with a growing private practice. She wants to offer a premium patient experience but is bogged down by admin. She's looking for a tool just like **{product_name}** to solve *{idea[:30]}...*"

    step2 = f"""
---
### Step 2: Customer Segments

#### {persona1_name}
* **Demographics:** {persona1_demo}
* **Psychographics:** {persona1_psych}
* **Buying Motivations:** To solve their immediate, high-priority problem.
* **Pain Points / Unmet Needs:** {persona1_pain}
* **Channels & Media Preferences:** Instagram, LinkedIn, Niche Communities (e.g., Discord, Reddit).
* **Price Sensitivity:** Medium.
* **Fit with Brand:** High.
* **Persona Summary:** {persona1_summary}
* **Generated Persona Image:**
    ![Persona 1]({img1_url})

#### {persona2_name}
* **Demographics:** {persona2_demo}
* **Psychographics:** {persona2_psych}
* **Buying Motivations:** To improve efficiency, save time, or for curiosity.
* **Pain Points / Unmet Needs:** {persona2_pain}
* **Channels & Media Preferences:** LinkedIn, Twitter/X, Zomato/Swiggy, Tech Blogs.
* **Price Sensitivity:** High / Medium.
* **Fit with Brand:** Medium to High.
* **Persona Summary:** {persona2_summary}
* **Generated Persona Image:**
    ![Persona 2]({img2_url})
"""

    # --- Step 3 ---
    step3 = f"""
---
### Step 3: Segment Prioritization
* **High-Priority Segment:**
    1.  **"{persona1_name.split(':')[-1].strip()}":** This group has the highest immediate need, clear buying intent, and (likely) the financial capacity to pay. They will be the best source of quality feedback for your beta in **{launch_city}**.
* **Key Marketing Message:** "Stop wasting time with old solutions. **{product_name}** is the new, intelligent way to solve *{idea[:30]}...* for busy **{ideal_customer}** like you."
"""

    # --- Step 4 ---
    step4 = f"""
---
### Step 4: Positioning Implication
* **Positioning:** Position **{product_name}** as the most "intelligent, practical, and personalized" solution for **{ideal_customer}** in India.
* **Tone of Voice:** Empowering, clear, and empathetic. Avoid jargon. Be the "smart assistant" they wish they had.
* **Visual Style Cues:** Clean, dark-mode first UI, bright, "intelligent" accent colors, and professional sans-serif fonts.
"""
    
    # --- Step 5 ---
    step5 = f"""
---
### Step 5: Risks / Overlooked Audiences
* **Risks:**
    * **Competition:** Free tools or "good enough" manual processes are your biggest competitors. The value must be 10x better.
    * **Data Privacy:** Be clear about how user data is (or isn't) used, especially if you're targeting sensitive fields like **{ideal_customer}**.
* **Overlooked Audience Opportunity:**
    * **Tier 2/3 Cities:** Don't just focus on **{launch_city}**. Ambitious **{ideal_customer}** in cities like Jaipur, Coimbatore, or Indore have high ambition but fewer tools.
"""
    
    # --- Combine and Return ---
    final_output = f"{step1}{step2}{step3}{step4}{step5}"
    return final_output


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
            with st.spinner("Generating your brand..."):
                time.sleep(2) # Simulate API call time
                segmentation_output = get_mock_segmentation_output(
                    st.session_state.startup_idea, 
                    st.session_state.startup_launch_plan # Pass updated variable
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


# --- 4. MAIN APPLICATION LOGIC ---

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
