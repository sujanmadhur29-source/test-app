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
    """
    # Use inputs to make the mock data feel dynamic
    product_name = idea.split(' ')[0].capitalize() if idea else "CodeTutor"
    launch_city = "Bangalore" # Default
    if "Bangalore" in launch_plan or "Bengaluru" in launch_plan:
        launch_city = "Bangalore"
    elif "Mumbai" in launch_plan:
        launch_city = "Mumbai"
    elif "Delhi" in launch_plan:
        launch_city = "Delhi"
    
    # Use placeholder images for personas
    img1_url = "https://placehold.co/300x300/E0E0E0/000000?text=Aarav+K."
    img2_url = "https://placehold.co/300x300/B0B0B0/000000?text=Priya+S."
    img3_url = "https://placehold.co/300x300/D0D0D0/000000?text=Rohan+G."

    mock_output = f"""
### Step 1: Primary Target Market
The primary target market is aspiring and early-career tech professionals in urban India (initially {launch_city}), aged 18-30, who are actively seeking to upskill in programming and need a flexible, on-demand learning tool to stay competitive.

---
### Step 2: Customer Segments

#### Segment 1: "The Ambitious Student"
* **Demographics:** 18-22, Male/Female, Low-income (student), Tier 1/2 city (e.g., {launch_city}, Pune, Hyderabad).
* **Psychographics:** Stressed about placements, values academic performance, FOMO, digitally native, seeks validation from peers.
* **Buying Motivations:** To pass difficult exams, build a project portfolio for their resume, get a high-paying internship/job.
* **Pain Points / Unmet Needs:** Cookie-cutter college curriculum, lack of personalized doubt-solving, expensive human tutors.
* **Channels & Media Preferences:** Instagram (Reels, memes), Discord (college servers), YouTube (tech tutorials), Telegram (notes sharing), LinkedIn (internship hunting).
* **Price Sensitivity:** High. (Relies on parent's money or scholarship)
* **Fit with Brand:** High.
* **Persona Summary (Aarav K.):** Aarav is a 3rd-year B.Tech student in {launch_city} juggling assignments and preparing for placements. He feels his college syllabus is outdated. He spends his evenings scrolling Instagram, watching Ankur Warikoo on YouTube, and trying to find clear explanations for complex Data Structures concepts. He needs a tool that can explain a bug in his code at 2 AM without him having to wait for a professor.
* **Generated Persona Image:**
    ![Persona of Aarav K.]({img1_url})

#### Segment 2: "The Early-Career Accelerator"
* **Demographics:** 23-28, Male/Female, Income ₹8L-₹15L, Tier 1 city ({launch_city}, Mumbai, Delhi).
* **Psychographics:** Career-focused, time-poor, values efficiency and ROI, invests in self-improvement, reads Finshots and TechCrunch.
* **Buying Motivations:** To get promoted, switch to a higher-paying domain (e.g., backend to data science), or join a FAANG/top-tier startup.
* **Pain Points / Unmet Needs:** Lacks time for long courses, needs specific answers to on-the-job problems, finds generic tutorials too basic.
* **Channels & Media Preferences:** LinkedIn (professional networking), Twitter/X (tech news), Zomato/Swiggy (daily convenience), Substack (niche newsletters).
* **Price Sensitivity:** Medium. (Willing to pay for clear value)
* **Fit with Brand:** High.
* **Persona Summary (Priya S.):** Priya is a Software Engineer with 2 years of experience at a {launch_city} startup. She's brilliant but feels stuck in a maintenance role. She wants to transition to a Machine Learning position. She gets home from work at 8 PM, orders dinner on Swiggy, and has about 90 minutes to study. She's frustrated by YouTube playlists and needs a mentor-like tool to guide her learning path and answer specific, advanced questions about her product: **{idea}**.
* **Generated Persona Image:**
    ![Persona of Priya S.]({img2_url})

#### Segment 3: "The Curious Hobbyist"
* **Demographics:** 28-40+, Any Gender, High Income (₹20L+), Tier 1 city.
* **Psychographics:** Lifelong learner, intellectually curious, may not be a professional developer, values user experience, enjoys tinkering.
* **Buying Motivations:** To build a personal project (e.g., a home automation script), understand new tech (like AI), or for pure intellectual stimulation.
* **Pain Points / Unmet Needs:** Intimidated by complex developer jargon, finds existing tools too "professional" and not "fun."
* **Channels & Media Preferences:** LinkedIn (as a thought leader), Blinkit (for convenience), The Ken/The Morning Context (for deep dives), attends tech meetups.
* **Price Sensitivity:** Low.
* **Fit with Brand:** Medium. (High long-term value, but not the primary target).
* **Persona Summary (Rohan G.):** Rohan is a Product Manager at a large e-commerce firm. He doesn't write code for his job but wants to learn Python to build his own generative AI app. He's tried a few courses but finds them dry. He's looking for a polished, intuitive tool that *feels* as good to use as the apps he designs, and can help him with his **{launch_plan}**-related side project.
* **Generated Persona Image:**
    ![Persona of Rohan G.]({img3_url})

---
### Step 3: Segment Prioritization
* **High-Priority Segments:**
    1.  **Segment 2: "The Early-Career Accelerator" (Priya S.):** This group has the highest immediate need, clear buying intent (career growth), and the financial capacity to pay for a subscription. They will be the best source of quality feedback for your beta.
    2.  **Segment 1: "The Ambitious Student" (Aarav K.):** This is your volume and future-user base. While price-sensitive, they are your brand advocates and will drive word-of-mouth growth in the long run.

* **Key Marketing Message (for both):** "Stop searching. Start building. Your personal AI coding mentor that understands your code, debugs your problems, and accelerates your career. From college placements to your next promotion."

---
### Step 4: Positioning Implication
* **Positioning:** Position the brand as the most "intelligent, practical, and personalized" AI learning partner for India's next generation of builders. Not just a "tutor," but a "collaborator."
* **Tone of Voice:** Empowering, clear, and empathetic. Avoid overly technical jargon. Be the "smart senior" you wish you had. (e.g., "We found a bug. Here's how to think about it, not just the answer.")
* **Visual Style Cues:** Clean, dark-mode first UI (like VS Code or Linear), bright, "intelligent" accent colors (e.g., electric blue, neon green), and professional but modern sans-serif fonts (like your app's 'Inter' font).

---
### Step 5: Risks / Overlooked Audiences
* **Risks:**
    * **Over-reliance on Generative AI:** Hallucinations or incorrect code can destroy trust. You *must* have a high accuracy and quality bar.
    * **Competition:** Free tools (Stack Overflow, ChatGPT) are the biggest competitors. The *personalization* and *structured learning paths* must be the key differentiators.
    * **Data Privacy:** Be clear about how users' code is (or isn't) used for training.
* **Overlooked Audience Opportunity:**
    * **Tier 2/3 City Students:** Don't just focus on {launch_city}. Students in cities like Jaipur, Coimbatore, or Indore have high ambition but even *less* access to quality mentorship. A mobile-first, low-bandwidth version could be a massive hit here.
"""
    return mock_output


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
