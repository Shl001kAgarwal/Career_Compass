import streamlit as st
import os
from utils.data_loader import load_initial_data

# Set page configuration
st.set_page_config(
    page_title="Career Compass - Career Recommendation System",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state variables if they don't exist
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'skills' not in st.session_state:
        st.session_state.skills = []
    if 'personality_results' not in st.session_state:
        st.session_state.personality_results = {}
    if 'career_recommendations' not in st.session_state:
        st.session_state.career_recommendations = []
    if 'skill_gaps' not in st.session_state:
        st.session_state.skill_gaps = {}
    if 'career_path' not in st.session_state:
        st.session_state.career_path = {}
    if 'courses' not in st.session_state:
        st.session_state.courses = []
    
    # Load initial data
    load_initial_data()
    
    # Application header
    st.title("🧭 Career Compass")
    st.subheader("AI-Powered Career Recommendation System")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        Welcome to Career Compass, your AI-powered career advisor. This system helps you:
        
        - Analyze your resume to extract relevant skills
        - Assess your personality and interests
        - Recommend optimal career paths that match your profile
        - Identify skill gaps and provide upskilling recommendations
        - Visualize potential career trajectories
        
        ### How to Use
        1. Upload your resume in the **Upload Resume** section
        2. Complete the **Skills Assessment** to refine your skill profile
        3. Take the **Personality Assessment** to factor in your interests
        4. Explore your personalized **Career Recommendations**
        5. Review **Skill Gap Analysis** to understand improvement areas
        6. Discover your potential **Career Trajectory**
        7. Find **Upskilling Recommendations** to enhance your prospects
        
        Get started by navigating through the pages on the sidebar!
        """)
    
    with col2:
        st.image("https://pixabay.com/get/g485182732aaac137c3ea8571bc30cede89998064a6a8dc5372740ff931a87caf15e0d86af19b716667bf4fee09acf00fa00e6c87d51081fb727c840cb7486649_1280.jpg", 
                 caption="Career Growth Path")
        
    # Display system status
    st.sidebar.title("System Status")
    
    # Create progress indicators for each step
    steps = [
        ("Resume Upload", bool(st.session_state.resume_data)),
        ("Skills Assessment", bool(st.session_state.skills)),
        ("Personality Assessment", bool(st.session_state.personality_results)),
        ("Career Recommendations", bool(st.session_state.career_recommendations)),
        ("Skill Gap Analysis", bool(st.session_state.skill_gaps)),
        ("Career Trajectory", bool(st.session_state.career_path)),
        ("Upskilling Recommendations", bool(st.session_state.courses))
    ]
    
    for step, completed in steps:
        if completed:
            st.sidebar.success(f"✅ {step} - Completed")
        else:
            st.sidebar.info(f"⏳ {step} - Pending")
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.subheader("About")
    st.sidebar.info(
        "Career Compass is an advanced career recommendation system that leverages "
        "machine learning, NLP, and data analysis to provide personalized career guidance. "
        "Built with Streamlit, pandas, scikit-learn, and other powerful Python libraries."
    )

if __name__ == "__main__":
    main()
