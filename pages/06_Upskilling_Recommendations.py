import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.recommendation_engine import create_user_profile
from utils.skill_analyzer import analyze_skill_gaps
from utils.course_recommender import recommend_courses, format_course_recommendations

st.set_page_config(
    page_title="Upskilling Recommendations - Career Compass",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 Upskilling Recommendations")
    st.write("Discover courses and resources to develop the skills you need for your target careers.")
    
    # Check if required data exists
    if not check_required_data():
        st.warning("Please complete the previous steps before viewing upskilling recommendations.")
        st.info("You need to complete the skills assessment and review career recommendations first.")
        return
    
    # Create user profile from all available data
    user_profile = create_user_profile(
        st.session_state.resume_data,
        st.session_state.skills,
        st.session_state.personality_results
    )
    
    # Extract user skills 
    user_skills = user_profile["technical_skills"] + user_profile["soft_skills"]
    
    # Check if skill gaps exist, if not, analyze them
    if "skill_gaps" not in st.session_state or not st.session_state.skill_gaps:
        with st.spinner("Analyzing skill gaps for recommended careers..."):
            # Analyze skill gaps for recommended careers
            skill_gaps = analyze_skill_gaps(user_skills, st.session_state.career_recommendations)
            st.session_state.skill_gaps = skill_gaps
    
    # Check if a specific career was selected
    selected_career = None
    selected_skill_gaps = None
    
    if "selected_career" in st.session_state and st.session_state.selected_career:
        selected_career = st.session_state.selected_career
        # Get skill gaps for this career
        selected_skill_gaps = st.session_state.skill_gaps.get(selected_career["title"])
        
        st.info(f"Showing upskilling recommendations for: {selected_career['title']}")
        
        # Allow changing the selection
        if st.button("Select a Different Career"):
            st.session_state.selected_career = None
            st.session_state.selected_skill_gaps = None
            st.rerun()
    
    # If no career is selected, let the user choose from recommendations
    if not selected_career:
        st.subheader("Select a Career to Explore")
        
        career_options = list(st.session_state.skill_gaps.keys())
        selected_title = st.selectbox(
            "Choose a career to view upskilling recommendations:",
            career_options
        )
        
        # Find the selected career object
        selected_career = next((rec for rec in st.session_state.career_recommendations 
                             if rec['title'] == selected_title), None)
        
        # Get skill gaps for this career
        selected_skill_gaps = st.session_state.skill_gaps.get(selected_title)
        
        if not selected_career or not selected_skill_gaps:
            st.error("Unable to find skill gap data for the selected career. Please try again.")
            return
        
        # Save selection to session state
        st.session_state.selected_career = selected_career
        st.session_state.selected_skill_gaps = selected_skill_gaps
    
    # Get or generate course recommendations for the selected career
    course_key = f"courses_{selected_career['title']}"
    
    if course_key not in st.session_state or not st.session_state[course_key]:
        with st.spinner(f"Finding course recommendations for {selected_career['title']}..."):
            # Get prioritized skills to develop
            if selected_skill_gaps and "prioritized_skills" in selected_skill_gaps:
                priority_skills = selected_skill_gaps["prioritized_skills"]
                
                # Recommend courses for these skills
                course_recommendations = recommend_courses(priority_skills, user_profile)
                
                # Format recommendations for display
                formatted_recommendations = format_course_recommendations(course_recommendations)
                
                # Save to session state
                st.session_state[course_key] = formatted_recommendations
            else:
                st.error("No prioritized skills found. Please try a different career.")
                return
    
    # Display course recommendations
    if course_key in st.session_state and st.session_state[course_key]:
        display_course_recommendations(
            st.session_state[course_key],
            selected_career,
            selected_skill_gaps
        )
    else:
        st.error("Unable to find course recommendations. Please try a different career.")

def check_required_data():
    """Check if the required data exists in session state"""
    # Need skills data
    if "skills" not in st.session_state or not st.session_state.skills:
        return False
    
    # Need career recommendations
    if "career_recommendations" not in st.session_state or not st.session_state.career_recommendations:
        return False
    
    return True

def display_course_recommendations(course_recommendations, selected_career, skill_gaps):
    """Display course recommendations to the user"""
    # Introduction section
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.image("https://pixabay.com/get/ge5799f39960949687c7b1d5d7f69efbfaf6e7a63aff73cdc28d0de056300046b7d23b29c04d9190de57ba2f6aad7ce8e4222918adee9144bebb97dcd6d3a3aa0_1280.jpg", 
                 caption="Skills Development")
    
    with col1:
        st.markdown(f"""
        ### Upskilling Recommendations for {selected_career['title']}
        
        Based on your skill gap analysis, we've identified the most important skills 
        to develop for this career path, along with targeted learning resources.
        
        These recommendations:
        
        - Focus on your highest priority skill gaps
        - Match your learning style and preferences
        - Include a mix of course formats and difficulty levels
        - Come from reputable learning platforms
        
        Use these resources to create your personal upskilling plan.
        """)
    
    # Display skill completion status
    completion_percentage = skill_gaps["completion_percentage"]
    skills_possessed = skill_gaps["skills_possessed"]
    total_required = skill_gaps["total_required"]
    
    st.metric(
        "Current Skill Completion", 
        f"{completion_percentage:.1f}%",
        f"{skills_possessed} of {total_required} skills"
    )
    
    # Create tabs for each priority skill
    priority_skills = skill_gaps["prioritized_skills"]
    
    if not priority_skills:
        st.success("Congratulations! You already have all the key skills needed for this role.")
        return
    
    # Filter course recommendations to only include skills with courses
    available_skills = [skill for skill in priority_skills if skill in course_recommendations]
    
    if not available_skills:
        st.warning("No specific course recommendations available for your skill gaps.")
        return
    
    # Create tabs for skills with recommendations
    skill_tabs = st.tabs([skill for skill in available_skills])
    
    for i, tab in enumerate(skill_tabs):
        skill = available_skills[i]
        skill_courses = course_recommendations[skill]
        
        with tab:
            display_skill_courses(skill, skill_courses)
    

    
    # Next steps
    st.subheader("Additional Resources")
    st.markdown("""
    Beyond formal courses, consider these additional ways to develop your skills:
    
    - **Professional communities**: Join forums, Slack groups, or meetups related to your target skills
    - **Open-source projects**: Contribute to projects that use technologies you want to learn
    - **Mentorship**: Find a mentor who works in your target role
    - **Side projects**: Create personal projects that demonstrate your new skills
    - **Shadowing**: Ask to shadow professionals in your target role
    """)
    
    # Navigation footer
    st.markdown("---")
    st.subheader("What's Next?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Skill Gap Analysis"):
            # Navigate to skill gap page
            pass
    with col2:
        if st.button("Return to Career Recommendations"):
            # Navigate back to recommendations page
            pass

def display_skill_courses(skill, courses):
    """Display course recommendations for a specific skill"""
    st.markdown(f"### Learning Resources for: {skill}")
    
    # Display courses in card format
    for i, course in enumerate(courses):
        with st.expander(f"{i+1}. {course['title']} ({course['provider']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{course['title']}**")
                st.markdown(f"**Provider:** {course['provider']}")
                st.markdown(f"**Description:** {course['description_short']}")
                st.markdown(f"**Format:** {course['format']}")
                st.markdown(f"**Duration:** {course['duration']}")
                st.markdown(f"**Difficulty:** {course['difficulty'].title()}")
                
                # Course URL as button
                st.markdown(f"[View Course]({course['url']})")
            
            with col2:
                st.markdown(f"**Cost:** {course['cost']}")
                
                # Visual indicator of difficulty
                difficulty_color = {
                    "beginner": "green",
                    "intermediate": "orange",
                    "advanced": "red"
                }.get(course['difficulty'].lower(), "gray")
                
                st.markdown(f"""
                <div style="background-color: {difficulty_color}; padding: 10px; 
                border-radius: 5px; color: white; text-align: center; margin-bottom: 10px;">
                {course['difficulty'].title()} Level
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
