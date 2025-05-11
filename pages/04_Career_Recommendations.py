import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.recommendation_engine import create_user_profile, recommend_careers, explain_recommendation

st.set_page_config(
    page_title="Career Recommendations - Career Compass",
    page_icon="🎯",
    layout="wide"
)

def main():
    st.title("🎯 Career Recommendations")
    st.write("Based on your skills, experience, and personality, here are your personalized career recommendations.")
    
    # Check if required data exists
    if not check_required_data():
        st.warning("Please complete the previous steps before viewing career recommendations.")
        st.info("You need to upload your resume and complete the skills and personality assessments.")
        return
    
    # Create user profile from all available data
    user_profile = create_user_profile(
        st.session_state.resume_data,
        st.session_state.skills,
        st.session_state.personality_results
    )
    
    # Generate career recommendations if not already present
    if "career_recommendations" not in st.session_state or not st.session_state.career_recommendations:
        with st.spinner("Analyzing your profile and generating career recommendations..."):
            # Get recommendations (default 5)
            recommendations = recommend_careers(user_profile, num_recommendations=5)
            st.session_state.career_recommendations = recommendations
    
    # Display recommendations
    if st.session_state.career_recommendations:
        display_recommendations(st.session_state.career_recommendations, user_profile)
    else:
        st.error("Unable to generate career recommendations. Please check your profile data.")

def check_required_data():
    """Check if the required data exists in session state"""
    # Need at least skills and personality data
    if "skills" not in st.session_state or not st.session_state.skills:
        return False
    
    if "personality_results" not in st.session_state or not st.session_state.personality_results:
        return False
    
    # Need at least some skills defined
    if (not st.session_state.skills.get("technical") and 
        not st.session_state.skills.get("soft")):
        return False
    
    # Need at least RIASEC from personality assessment
    if "riasec" not in st.session_state.personality_results:
        return False
    
    return True

def display_recommendations(recommendations, user_profile):
    """Display career recommendations to the user"""
    st.subheader("Top Career Matches")
    
    # Display header image
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.image("https://pixabay.com/get/g973d4124f27cb5da2edefb0c23537d915e4bbf48f1b66b110edfae6bf87f228ae5a68ab00cc36ec9a28a1edd6dcd9c7c0e35c0effcbf05137292f593f94fdf09_1280.jpg", 
                 caption="Career professionals")
    
    with col1:
        st.markdown("""
        ### Your Career Match Results
        
        Based on your unique profile of skills, experience, and personality traits, we've identified the careers 
        that best match your strengths and interests.
        
        For each recommendation, we provide:
        - Match score showing compatibility
        - Salary range and growth outlook
        - Required education level
        - Matching and missing skills
        - Detailed explanation of why this career was recommended
        
        Select any career to explore details and next steps.
        """)
    
    # Create tabs for each recommendation
    tabs = st.tabs([f"{rec['title']} ({rec['match_score']}%)" for rec in recommendations])
    
    for i, tab in enumerate(tabs):
        recommendation = recommendations[i]
        
        with tab:
            display_career_details(recommendation, user_profile)
    
    # Career comparison section
    st.subheader("Career Comparison")
    
    # Salary comparison chart
    st.markdown("#### Salary Comparison")
    salary_data = pd.DataFrame({
        'Career': [rec['title'] for rec in recommendations],
        'Minimum': [rec['salary_range']['min'] for rec in recommendations],
        'Median': [rec['salary_range']['median'] for rec in recommendations],
        'Maximum': [rec['salary_range']['max'] for rec in recommendations]
    })
    
    fig = px.bar(salary_data, x='Career', y=['Minimum', 'Median', 'Maximum'],
                barmode='group', title="Salary Range Comparison",
                labels={'value': 'Annual Salary ($)', 'variable': 'Salary Point'})
    
    st.plotly_chart(fig, key="salary_comparison")
    
    # Skill match comparison chart
    st.markdown("#### Skill Match Comparison")
    
    skill_match_data = pd.DataFrame({
        'Career': [rec['title'] for rec in recommendations],
        'Match Score': [rec['match_score'] for rec in recommendations],
        'Skill Match': [rec['skill_match_percentage'] for rec in recommendations]
    })
    
    fig = px.bar(skill_match_data, x='Career', y=['Match Score', 'Skill Match'],
                barmode='group', title="Career Match Score Comparison",
                labels={'value': 'Percentage (%)', 'variable': 'Metric'})
    
    st.plotly_chart(fig, key="skill_comparison")
    
    # Top companies hiring comparison
    st.markdown("#### Top Companies Hiring")
    
    # Create a list of top companies for each career
    company_data = []
    for rec in recommendations:
        if 'top_companies' in rec and rec['top_companies']:
            # Take top 2 companies from each career
            for i, company in enumerate(rec['top_companies'][:2]):
                try:
                    company_data.append({
                        'Career': rec['title'],
                        'Company': company['name'],
                        'Avg. Salary': company['avg_salary'],
                        'Location': company['location'],
                        'Hiring Frequency': company['hiring_frequency']
                    })
                except (KeyError, TypeError) as e:
                    st.warning(f"Error adding company data: {str(e)}")
    
    if company_data:
        company_df = pd.DataFrame(company_data)
        
        # Create a scatter plot of companies by hiring frequency and salary
        fig = px.scatter(
            company_df, 
            x='Hiring Frequency', 
            y='Avg. Salary',
            color='Career',
            size='Hiring Frequency',
            hover_name='Company',
            hover_data=['Location'],
            title="Top Companies by Hiring Frequency and Salary",
            labels={'Avg. Salary': 'Average Salary ($)'}
        )
        
        st.plotly_chart(fig, key="company_comparison")
        
        # Also show as a table
        with st.expander("View Company Hiring Data"):
            # Create a copy of the dataframe
            display_df = company_df.copy()
            # Display the dataframe
            st.dataframe(display_df)
    
    # Next steps
    st.subheader("Next Steps")
    st.markdown("""
    Now that you've reviewed your career matches, here are the next steps:
    
    1. **Explore Skill Gaps**: Understand what skills you need to develop for each career
    2. **View Career Trajectories**: See potential career progression paths for each role
    3. **Get Upskilling Recommendations**: Find specific courses to build required skills
    """)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View Skill Gap Analysis"):
            # Navigate to skill gap page
            pass
    with col2:
        if st.button("Explore Career Trajectories"):
            # Navigate to career trajectory page
            pass
    with col3:
        if st.button("Find Upskilling Opportunities"):
            # Navigate to upskilling page
            pass

def display_career_details(recommendation, user_profile):
    """Display detailed information for a career recommendation"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Career title and description
        st.markdown(f"## {recommendation['title']}")
        st.write(recommendation['description'])
        
        # Explain recommendation
        st.subheader("Why This Career Matches Your Profile")
        explanation = explain_recommendation(recommendation)
        st.markdown(explanation)
        
        # Education required
        st.subheader("Required Education")
        st.info(recommendation['education_required'])
        
        # Growth outlook
        st.subheader("Career Outlook")
        outlook = recommendation['growth_outlook']
        
        # Determine color based on outlook
        if "much faster" in outlook.lower():
            st.success(f"📈 {outlook}")
        elif "faster" in outlook.lower():
            st.success(f"📈 {outlook}")
        elif "average" in outlook.lower():
            st.info(f"⟷ {outlook}")
        else:
            st.warning(f"📉 {outlook}")
            
        # Top companies hiring for this role
        if 'top_companies' in recommendation and recommendation['top_companies']:
            st.subheader("Top Companies Hiring")
            company_data = pd.DataFrame(recommendation['top_companies'])
            
            # Create a bar chart of top companies by hiring frequency
            fig_companies = px.bar(
                company_data.head(5), 
                x='name', 
                y='hiring_frequency',
                color='avg_salary',
                color_continuous_scale='Viridis',
                title=f"Top Companies Hiring for {recommendation['title']}",
                labels={
                    'name': 'Company',
                    'hiring_frequency': 'Hiring Frequency',
                    'avg_salary': 'Average Salary ($)'
                }
            )
            
            # Customize the chart
            fig_companies.update_layout(
                xaxis_tickangle=-45,
                coloraxis_colorbar=dict(title="Avg Salary ($)")
            )
            
            st.plotly_chart(fig_companies, key=f"companies_{recommendation['code']}")
            
            # Show company details in an expandable section
            with st.expander("View Company Details"):
                # Create a copy of the dataframe with selected columns
                df_details = company_data[['name', 'location', 'avg_salary']].copy()
                
                # Rename columns
                df_details.columns = ['Company', 'Location', 'Average Salary']
                
                # Set index and display
                st.dataframe(df_details.set_index('Company'))
    
    with col2:
        # Match score gauge chart
        match_score = recommendation['match_score']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = match_score,
            title = {'text': "Match Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "lightblue"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig, key=f"match_gauge_{recommendation['code']}")
        
        # Salary range
        st.subheader("Salary Range")
        
        salary_min = recommendation['salary_range']['min']
        salary_max = recommendation['salary_range']['max']
        salary_median = recommendation['salary_range']['median']
        
        st.metric("Median Annual Salary", f"${salary_median:,}")
        
        salary_data = pd.DataFrame({
            'Range': ['Minimum', 'Median', 'Maximum'],
            'Salary': [salary_min, salary_median, salary_max]
        })
        
        fig = px.bar(salary_data, x='Range', y='Salary',
                    title="Salary Range",
                    labels={'Salary': 'Annual Salary ($)'})
        
        st.plotly_chart(fig, key=f"salary_bar_{recommendation['code']}")
        
        # Skill match
        st.subheader("Skill Match")
        
        # Extract skill match data
        matching_skills = recommendation['matching_skills']
        missing_skills = recommendation['missing_skills']
        match_percentage = recommendation['skill_match_percentage']
        
        # Display skill match percentage
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = match_percentage,
            title = {'text': "Skill Match"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ]
            }
        ))
        
        st.plotly_chart(fig, key=f"skill_gauge_{recommendation['code']}")
    
    # Skills section
    st.subheader("Skills Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Skills You Have")
        if matching_skills:
            # Display matching skills as pills
            html_skills = ""
            for skill in matching_skills[:10]:  # Show top 10 to avoid clutter
                html_skills += f'<span style="background-color:#1E88E5;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
            st.markdown(html_skills, unsafe_allow_html=True)
            
            if len(matching_skills) > 10:
                st.write(f"...and {len(matching_skills) - 10} more skills")
        else:
            st.info("No directly matching skills identified.")
    
    with col2:
        st.markdown("#### Skills to Develop")
        if missing_skills:
            # Display missing skills as pills
            html_skills = ""
            for skill in missing_skills[:10]:  # Show top 10 to avoid clutter
                html_skills += f'<span style="background-color:#F44336;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
            st.markdown(html_skills, unsafe_allow_html=True)
            
            if len(missing_skills) > 10:
                st.write(f"...and {len(missing_skills) - 10} more skills")
        else:
            st.success("You have all the key skills for this role!")
    
    # Next steps specific to this career
    st.subheader("Next Steps for This Career")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"View Skill Gaps for {recommendation['title']}", key=f"gaps_{recommendation['code']}"):
            # Store selected career and navigate
            st.session_state.selected_career = recommendation
            # Navigate to skill gap page
            pass
    
    with col2:
        if st.button(f"See Career Path for {recommendation['title']}", key=f"path_{recommendation['code']}"):
            # Store selected career and navigate
            st.session_state.selected_career = recommendation
            # Navigate to career trajectory page
            pass
    
    with col3:
        if st.button(f"Find Courses for {recommendation['title']}", key=f"course_{recommendation['code']}"):
            # Store selected career and navigate
            st.session_state.selected_career = recommendation
            # Navigate to upskilling page
            pass

if __name__ == "__main__":
    main()
