import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.recommendation_engine import create_user_profile, recommend_careers
from utils.skill_analyzer import analyze_skill_gaps, recommend_skill_development_paths

st.set_page_config(
    page_title="Skill Gap Analysis - Career Compass",
    page_icon="🔍",
    layout="wide"
)

def main():
    st.title("🔍 Skill Gap Analysis")
    st.write("Understand the skills you need to develop for your targeted career paths.")
    
    # Check if required data exists
    if not check_required_data():
        st.warning("Please complete the previous steps before viewing skill gap analysis.")
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
    
    # Analyze skill gaps if not already present
    if "skill_gaps" not in st.session_state or not st.session_state.skill_gaps:
        with st.spinner("Analyzing skill gaps for recommended careers..."):
            # Analyze skill gaps for recommended careers
            skill_gaps = analyze_skill_gaps(user_skills, st.session_state.career_recommendations)
            st.session_state.skill_gaps = skill_gaps
            
            # Generate skill development paths
            development_paths = recommend_skill_development_paths(skill_gaps, user_profile)
            st.session_state.development_paths = development_paths
    
    # Display skill gap analysis
    if st.session_state.skill_gaps and st.session_state.development_paths:
        display_skill_gap_analysis(
            st.session_state.skill_gaps,
            st.session_state.development_paths,
            st.session_state.career_recommendations,
            user_skills
        )
    else:
        st.error("Unable to analyze skill gaps. Please check your profile data and career recommendations.")

def check_required_data():
    """Check if the required data exists in session state"""
    # Need skills data
    if "skills" not in st.session_state or not st.session_state.skills:
        return False
    
    # Need career recommendations
    if "career_recommendations" not in st.session_state or not st.session_state.career_recommendations:
        return False
    
    # Need at least some skills defined
    if (not st.session_state.skills.get("technical") and 
        not st.session_state.skills.get("soft")):
        return False
    
    return True

def display_skill_gap_analysis(skill_gaps, development_paths, recommendations, user_skills):
    """Display skill gap analysis to the user"""
    # Introduction section
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.image("https://pixabay.com/get/gb066bdb24fef8342ab8fda4cf5be23854380de21f881a048f3971e0e335e3bc38ff1fb02c216fd263319a37b836a7493f120a191ba49460b3e5f89279b539782_1280.jpg", 
                 caption="Career Growth Path")
    
    with col1:
        st.markdown("""
        ### Understanding Your Skill Gaps
        
        This analysis compares your current skills with those required for each recommended career path.
        Understanding these gaps helps you:
        
        - Identify specific skills to develop
        - Prioritize your learning journey
        - Create targeted upskilling plans
        - Estimate time needed to prepare for career transitions
        
        Use this information to make strategic decisions about your career development.
        """)
    
    # Overall comparison chart
    st.subheader("Skill Completion Overview")
    
    # Prepare data for the chart
    completion_data = []
    for career, gap_data in skill_gaps.items():
        completion_data.append({
            "Career": career,
            "Skills Possessed": gap_data["skills_possessed"],
            "Skills Missing": gap_data["total_required"] - gap_data["skills_possessed"],
            "Completion Percentage": gap_data["completion_percentage"]
        })
    
    completion_df = pd.DataFrame(completion_data)
    
    # Sort by completion percentage
    completion_df = completion_df.sort_values("Completion Percentage", ascending=True)
    
    # Create stacked bar chart for skills
    fig = px.bar(completion_df, x="Career", y=["Skills Possessed", "Skills Missing"],
                title="Skills Possessed vs Missing by Career",
                labels={"value": "Number of Skills", "variable": "Category"},
                barmode="stack")
    
    st.plotly_chart(fig)
    
    # Create completion percentage chart
    fig = px.bar(completion_df, x="Career", y="Completion Percentage",
                title="Skill Completion Percentage by Career",
                labels={"Completion Percentage": "Completion (%)"},
                color="Completion Percentage",
                color_continuous_scale=["red", "yellow", "green"])
    
    st.plotly_chart(fig)
    
    # Select a career to analyze
    st.subheader("Detailed Skill Gap Analysis")
    selected_career = st.selectbox(
        "Select a career to view detailed skill gap analysis:",
        list(skill_gaps.keys())
    )
    
    if selected_career:
        display_detailed_gap_analysis(
            selected_career,
            skill_gaps[selected_career],
            development_paths[selected_career],
            user_skills
        )
    
    # Next steps
    st.subheader("Next Steps")
    st.markdown("""
    Now that you understand your skill gaps, here are recommended next steps:
    
    1. **Explore Career Trajectories**: See how your career could evolve after addressing these skill gaps
    2. **Get Upskilling Recommendations**: Find specific courses to build your missing skills
    3. **Return to Career Recommendations**: Review other potential career matches
    """)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Explore Career Trajectories"):
            # Navigate to career trajectory page
            pass
    with col2:
        if st.button("Find Upskilling Opportunities"):
            # Navigate to upskilling page
            pass
    with col3:
        if st.button("Return to Career Recommendations"):
            # Navigate back to recommendations page
            pass

def display_detailed_gap_analysis(career_title, gap_data, development_path, user_skills):
    """Display detailed skill gap analysis for a selected career"""
    # Extract data
    completion_percentage = gap_data["completion_percentage"]
    skills_possessed = gap_data["skills_possessed"]
    total_required = gap_data["total_required"]
    missing_skills = gap_data["missing_skills"]
    prioritized_skills = gap_data["prioritized_skills"]
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"### Skill Gap Analysis for {career_title}")
        
        # Completion metrics
        st.metric(
            "Skill Completion", 
            f"{completion_percentage:.1f}%",
            f"{skills_possessed} of {total_required} skills"
        )
        
        # Display categorized missing skills
        if missing_skills:
            st.markdown("#### Skills to Develop")
            
            # Technical skills
            if missing_skills.get("technical"):
                st.write("**Technical Skills:**")
                tech_html = ""
                for skill in missing_skills["technical"][:10]:
                    tech_html += f'<span style="background-color:#F44336;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
                st.markdown(tech_html, unsafe_allow_html=True)
                
                if len(missing_skills["technical"]) > 10:
                    st.write(f"...and {len(missing_skills['technical']) - 10} more technical skills")
            
            # Abilities
            if missing_skills.get("abilities"):
                st.write("**Abilities:**")
                abilities_html = ""
                for skill in missing_skills["abilities"][:10]:
                    abilities_html += f'<span style="background-color:#FF9800;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
                st.markdown(abilities_html, unsafe_allow_html=True)
                
                if len(missing_skills["abilities"]) > 10:
                    st.write(f"...and {len(missing_skills['abilities']) - 10} more abilities")
            
            # Knowledge
            if missing_skills.get("knowledge"):
                st.write("**Knowledge Areas:**")
                knowledge_html = ""
                for skill in missing_skills["knowledge"][:10]:
                    knowledge_html += f'<span style="background-color:#4CAF50;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
                st.markdown(knowledge_html, unsafe_allow_html=True)
                
                if len(missing_skills["knowledge"]) > 10:
                    st.write(f"...and {len(missing_skills['knowledge']) - 10} more knowledge areas")
        else:
            st.success("You have all the required skills for this career!")
        
        # Display skill development path
        st.markdown("### Development Strategy")
        
        # Display estimated time
        time_estimate = development_path["estimated_time"]
        st.write(f"**Estimated Development Time:** {time_estimate['total_months']} months")
        st.write(f"**Time Frame:** {time_estimate['time_frame']}")
        st.write(f"**Recommended Intensity:** {time_estimate['intensity']}")
        
        # Display development strategies
        st.markdown("#### Recommended Learning Approach")
        for strategy in development_path["development_strategy"]:
            st.write(f"**{strategy['type'].replace('_', ' ').title()}:** {strategy['description']}")
    
    with col2:
        # Skill gap gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = completion_percentage,
            title = {'text': f"Skill Completeness for {career_title}"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 30], 'color': "red"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "green"}
                ]
            }
        ))
        
        st.plotly_chart(fig)
        
        # Priority skills to develop
        st.markdown("#### Priority Skills to Develop")
        st.info("These are the most important skills to focus on first")
        
        for i, skill in enumerate(prioritized_skills[:5], 1):
            st.write(f"{i}. **{skill}**")
        
        # Create pie chart for skill categories
        if missing_skills:
            categories = {}
            for category, skills in missing_skills.items():
                categories[category] = len(skills)
            
            if categories:
                labels = list(categories.keys())
                values = list(categories.values())
                
                fig = px.pie(
                    values=values, 
                    names=labels, 
                    title="Missing Skills by Category",
                    color=labels,
                    color_discrete_map={
                        'technical': '#F44336',
                        'abilities': '#FF9800',
                        'knowledge': '#4CAF50'
                    }
                )
                
                st.plotly_chart(fig)
    
    # Action buttons for this career
    st.markdown("### Take Action")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"View Career Path for {career_title}", key=f"path_{career_title}"):
            # Store selected career and navigate
            for rec in st.session_state.career_recommendations:
                if rec["title"] == career_title:
                    st.session_state.selected_career = rec
                    break
            # Navigate to career trajectory page
            pass
    
    with col2:
        if st.button(f"Find Courses for {career_title}", key=f"courses_{career_title}"):
            # Store selected career and skill gaps
            for rec in st.session_state.career_recommendations:
                if rec["title"] == career_title:
                    st.session_state.selected_career = rec
                    break
            st.session_state.selected_skill_gaps = gap_data
            # Navigate to upskilling page
            pass

if __name__ == "__main__":
    main()
