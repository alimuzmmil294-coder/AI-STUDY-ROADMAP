import os
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="AI Study Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cleaner typography and layout
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to load API Key from Streamlit Secrets, Environment Variables, or Sidebar Input
def get_api_key():
    # 1. Check Streamlit Cloud Secrets
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"], True
    except FileNotFoundError:
        pass

    # 2. Check OS Environment Variable (useful for local dev)
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key, True

    return "", False

configured_key, is_preconfigured = get_api_key()

# Sidebar for API Configuration and User Preferences
with st.sidebar:
    st.header("🔑 API Configuration")
    
    if is_preconfigured:
        st.success("✅ Gemini API Key loaded from Streamlit Secrets.")
        override_key = st.text_input(
            "Override API Key (Optional)",
            type="password",
            placeholder="Leave blank to use default secret"
        )
        api_key = override_key.strip() if override_key.strip() else configured_key
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter your AIza... key",
            help="Get your free API key from Google AI Studio."
        )
    
    st.divider()
    st.header("⚙️ Model Settings")
    model_choice = st.selectbox(
        "Select Gemini Model",
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Flash is faster and ideal for standard plans; Pro excels at deeply technical or multi-month curricula."
    )
    
    st.divider()
    st.markdown("### 💡 How it works")
    st.markdown(
        "1. Ensure your **Gemini API Key** is set.\n"
        "2. Enter the **Subject/Tech** you want to master.\n"
        "3. Define your **Timeframe** and **Daily Commitment**.\n"
        "4. Generate and download your custom roadmap."
    )

# Main Application Interface
st.markdown('<div class="main-header">🗺️ AI Study Roadmap Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform any topic and timeframe into a structured, actionable learning curriculum.</div>', unsafe_allow_html=True)

# Input Form
with st.form("study_planner_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "Tech Stack / Subject *",
            placeholder="e.g., Data Structures in C++, React.js, Linear Algebra, MERN Stack"
        )
        current_level = st.selectbox(
            "Current Knowledge Level",
            options=["Complete Beginner", "Basic Understanding", "Intermediate", "Advanced (Looking to Master)"]
        )
        learning_style = st.multiselect(
            "Preferred Focus Areas",
            options=[
                "Hands-on Projects",
                "Theoretical Foundations",
                "Documentation & Reading",
                "Video Tutorials",
                "Practice Problems / Exercises",
                "Interview Prep"
            ],
            default=["Hands-on Projects", "Theoretical Foundations"]
        )

    with col2:
        duration = st.text_input(
            "Total Timeframe *",
            placeholder="e.g., 4 weeks, 3 months, 10 days"
        )
        daily_hours = st.slider(
            "Daily Study Commitment (Hours)",
            min_value=0.5,
            max_value=12.0,
            value=2.0,
            step=0.5
        )
        specific_goals = st.text_area(
            "Specific Goals or Constraints (Optional)",
            placeholder="e.g., Prepare for university midterms, build a full-stack capstone project, skip basic HTML/CSS...",
            height=105
        )

    submitted = st.form_submit_button("🚀 Generate Study Roadmap", use_container_width=True, type="primary")

# Generation Logic
if submitted:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar (or configure `GEMINI_API_KEY` in Streamlit Secrets).")
    elif not topic.strip() or not duration.strip():
        st.warning("⚠️ Please fill in both the **Tech Stack / Subject** and **Total Timeframe** fields.")
    else:
        with st.spinner(f"Designing your custom {duration} roadmap for {topic}..."):
            try:
                client = genai.Client(api_key=api_key)
                
                focus_str = ", ".join(learning_style) if learning_style else "Balanced theory and practice"
                goals_str = specific_goals.strip() if specific_goals.strip() else "General mastery and practical competence"

                prompt = f"""
                Create a comprehensive, realistic, and actionable study roadmap based on the following parameters:
                
                - **Subject / Technology:** {topic}
                - **Total Timeframe:** {duration}
                - **Daily Time Commitment:** {daily_hours} hours per day
                - **Current Skill Level:** {current_level}
                - **Preferred Focus Areas:** {focus_str}
                - **Specific Goals / Constraints:** {goals_str}
                
                Please structure the roadmap using clear Markdown with the following sections:
                1. **Executive Overview & Realistic Expectations:** What the learner will realistically achieve in {duration} at {daily_hours} hrs/day.
                2. **Prerequisites & Setup:** Tools, environments, or foundational concepts needed on Day 1.
                3. **Phase-by-Phase / Week-by-Week Breakdown:** Break the timeline down logically (e.g., by days if less than 2 weeks, or by weeks/phases if longer). For each block, specify:
                   - Core Topics & Concepts
                   - Time Allocation
                   - Actionable Tasks / Exercises
                4. **Milestone Projects:** 2–3 concrete projects scaled to their level to cement knowledge.
                5. **Curated Resource Recommendations:** Types of documentation, official guides, or classic references to consult (avoid dead or hallucinated URLs; name official docs, books, or platforms).
                6. **Study & Retention Tips:** Tailored advice to avoid burnout and retain the material.
                """

                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are an expert curriculum designer, senior software engineer, and academic mentor. "
                            "Build practical, well-paced study roadmaps that strictly respect the user's daily hour constraints. "
                            "Avoid fluff and ensure every phase has clear deliverables."
                        ),
                        temperature=0.7,
                    )
                )

                st.success("✅ Roadmap generated successfully!")
                st.divider()
                
                # Display Roadmap
                st.markdown(response.text)
                
                st.divider()
                
                # Download Button for Markdown Export
                safe_filename = f"{topic.lower().replace(' ', '_')}_roadmap.md"
                st.download_button(
                    label="📥 Download Roadmap as Markdown (.md)",
                    data=response.text,
                    file_name=safe_filename,
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"❌ An error occurred while communicating with Gemini: {str(e)}")
