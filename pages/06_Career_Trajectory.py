import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.recommendation_engine import create_user_profile
from utils.career_trajectory import predict_career_trajectory

st.set_page_config(
    page_title="Career Trajectory - Career Compass",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 Career Trajectory")
    st.write("Explore how your career could evolve over time based on your current profile and interests.")
    
    # Check if required data exists
    if not check_required_data():
        st.warning("Please complete the previous steps before exploring career trajectories.")
        st.info("You need to complete the skills assessment and review career recommendations first.")
        return
    
    # Create user profile from all available data
    user_profile = create_user_profile(
        st.session_state.resume_data,
        st.session_state.skills,
        st.session_state.personality_results
    )
    
    # Check if a specific career was selected
    selected_career = None
    if "selected_career" in st.session_state and st.session_state.selected_career:
        selected_career = st.session_state.selected_career
        st.info(f"Showing career trajectory for: {selected_career['title']}")
        
        # Allow changing the selection
        if st.button("Select a Different Career"):
            st.session_state.selected_career = None
            st.rerun()
    
    # If no career is selected, let the user choose from recommendations
    if not selected_career:
        st.subheader("Select a Career to Explore")
        
        career_options = [rec['title'] for rec in st.session_state.career_recommendations]
        selected_title = st.selectbox(
            "Choose a starting career path:",
            career_options
        )
        
        # Find the selected career object
        selected_career = next((rec for rec in st.session_state.career_recommendations 
                             if rec['title'] == selected_title), None)
        
        if not selected_career:
            st.error("Unable to find the selected career. Please try again.")
            return
        
        # Save selection to session state
        st.session_state.selected_career = selected_career
    
    # Predict career trajectory if not already present or if career has changed
    career_path_key = f"career_path_{selected_career['title']}"
    if (career_path_key not in st.session_state or not st.session_state[career_path_key]):
        with st.spinner(f"Predicting career trajectory for {selected_career['title']}..."):
            # Predict trajectory for the selected career
            trajectory = predict_career_trajectory(selected_career['title'], user_profile)
            st.session_state[career_path_key] = trajectory
    
    # Display career trajectory
    if career_path_key in st.session_state and st.session_state[career_path_key]:
        display_career_trajectory(st.session_state[career_path_key])
    else:
        st.error("Unable to predict career trajectory. Please try a different career.")

def check_required_data():
    """Check if the required data exists in session state"""
    # Need skills data
    if "skills" not in st.session_state or not st.session_state.skills:
        return False
    
    # Need career recommendations
    if "career_recommendations" not in st.session_state or not st.session_state.career_recommendations:
        return False
    
    # Need personality data
    if "personality_results" not in st.session_state or not st.session_state.personality_results:
        return False
    
    return True

def display_career_trajectory(trajectory):
    """Display career trajectory visualization and details"""
    st.subheader(f"Career Trajectory: {trajectory['starting_role']}")
    
    # Introduction section
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.image("https://pixabay.com/get/g485182732aaac137c3ea8571bc30cede89998064a6a8dc5372740ff931a87caf15e0d86af19b716667bf4fee09acf00fa00e6c87d51081fb727c840cb7486649_1280.jpg", 
                 caption="Career Growth Path")
    
    with col1:
        st.markdown("""
        ### Your Career Evolution
        
        This analysis predicts how your career might evolve over the next 10 years
        based on common progression patterns in this field.
        
        We show you:
        
        - Multiple potential career paths
        - Salary progression over time
        - Required skills for each stage
        - Probability of each path
        
        Use this information to strategically plan your long-term career development.
        """)
    
    # Time horizon
    time_horizon = trajectory['time_horizon']
    year_labels = [f"Year {i}" for i in range(time_horizon + 1)]
    
    # Career paths visualization
    st.markdown("### Career Path Visualization")
    
    # Path tabs
    path_tabs = st.tabs([f"Path {i+1} ({path['probability']:.0%} probability)" 
                         for i, path in enumerate(trajectory['paths'])])
    
    for i, tab in enumerate(path_tabs):
        path = trajectory['paths'][i]
        
        with tab:
            display_career_path(path, year_labels, i)
    
    # Salary progression comparison
    st.subheader("Salary Progression Comparison")
    
    # Create salary data for all paths
    salary_data = []
    for path_idx, path in enumerate(trajectory['paths']):
        for year, role in enumerate(path['path_details']):
            if year <= time_horizon:  # Only include years within the time horizon
                salary_data.append({
                    'Path': f"Path {path_idx+1}",
                    'Year': f"Year {year}",
                    'Salary': role['salary'],
                    'Role': role['title']
                })
    
    # Create dataframe
    salary_df = pd.DataFrame(salary_data)
    
    # Plot salary progression
    fig = px.line(salary_df, x='Year', y='Salary', color='Path',
                 title="Salary Progression by Career Path",
                 labels={'Salary': 'Annual Salary ($)'},
                 markers=True)
    
    # Add hover information
    fig.update_traces(
        hovertemplate='<b>%{text}</b><br>Salary: $%{y:,.0f}<extra></extra>',
        text=salary_df['Role']
    )
    
    st.plotly_chart(fig)
    
    # Explanation of methodology
    st.markdown("### Methodology")
    st.markdown("""
    #### How These Trajectories Are Calculated
    
    These career trajectories are predicted using a combination of:
    
    1. **Historical career progression data** from similar profiles
    2. **Transition probability analysis** between related roles
    3. **Your personal skills and education** which may accelerate certain paths
    
    The probabilities represent the likelihood of a particular path based on common patterns and your profile.
    
    #### Factors That Can Influence Your Path
    
    Your actual career progression may be influenced by:
    - The speed at which you acquire new skills
    - Geographic location and job market conditions
    - Industry changes and emerging roles
    - Your personal preferences and choices
    
    Use these projections as a strategic planning tool, not a fixed prediction.
    """)
    
    # Next steps
    st.subheader("Next Steps")
    st.markdown("""
    Based on your career trajectory analysis, consider these next steps:
    
    1. **Identify Skill Gaps**: Review what skills you'll need for future roles
    2. **Find Upskilling Opportunities**: Take courses to prepare for career progression
    3. **Return to Career Recommendations**: Explore other potential career paths
    """)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Analyze Skill Gaps"):
            # Navigate to skill gap page
            pass
    with col2:
        if st.button("Find Upskilling Opportunities"):
            # Navigate to upskilling page
            pass
    with col3:
        if st.button("Return to Career Recommendations"):
            # Navigate back to recommendations page
            pass

def display_career_path(path, year_labels, path_index):
    """Display a specific career path"""
    path_details = path['path_details']
    probability = path['probability']
    description = path['description']
    
    # Display path description
    st.markdown(f"**Path Description:** {description}")
    st.markdown(f"**Probability:** {probability:.0%}")
    
    # Create role progression timeline
    role_timeline = []
    for i, role in enumerate(path_details):
        role_timeline.append({
            'Year': year_labels[i],
            'Role': role['title'],
            'Salary': role['salary'],
            'Education': role['education'],
            'Skills': ', '.join(role['skills_required'][:3]) + (', ...' if len(role['skills_required']) > 3 else '')
        })
    
    # Convert to dataframe for display
    timeline_df = pd.DataFrame(role_timeline)
    
    # Create a horizontal timeline visualization
    fig = go.Figure()
    
    # Add roles as markers
    fig.add_trace(go.Scatter(
        x=timeline_df['Year'],
        y=[1] * len(timeline_df),
        mode='markers+text',
        marker=dict(
            symbol='circle',
            size=20,
            color='blue',
            line=dict(
                color='white',
                width=2
            )
        ),
        text=timeline_df['Role'],
        textposition='bottom center',
        hoverinfo='text',
        hovertext=[f"<b>{row['Role']}</b><br>Salary: ${row['Salary']:,.0f}<br>Education: {row['Education']}<br>Key Skills: {row['Skills']}" 
                   for _, row in timeline_df.iterrows()]
    ))
    
    # Add connecting lines
    fig.add_trace(go.Scatter(
        x=timeline_df['Year'],
        y=[1] * len(timeline_df),
        mode='lines',
        line=dict(color='blue', width=2),
        hoverinfo='none'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Career Path {path_index + 1} Timeline",
        xaxis=dict(title='Year'),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, 2]
        ),
        height=300,
        margin=dict(l=20, r=20, t=50, b=50),
        hovermode='closest'
    )
    
    st.plotly_chart(fig)
    
    # Display detailed information for each role
    st.markdown("### Role Details")
    
    # Create expandable sections for each role
    for i, role in enumerate(path_details):
        with st.expander(f"Year {i}: {role['title']} (${role['salary']:,}/year)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Role:** {role['title']}")
                st.markdown(f"**Typical Salary:** ${role['salary']:,}")
                st.markdown(f"**Education Required:** {role['education']}")
            
            with col2:
                st.markdown("**Key Skills Required:**")
                for skill in role['skills_required']:
                    st.markdown(f"- {skill}")
            
            # Show transition info if not the last role
            if i < len(path_details) - 1:
                next_role = path_details[i + 1]
                
                # If role changes, show transition info
                if role['title'] != next_role['title']:
                    st.markdown("---")
                    st.markdown("#### Transition to Next Role")
                    
                    # Calculate skills needed for transition
                    current_skills = set(role['skills_required'])
                    next_skills = set(next_role['skills_required'])
                    new_skills = next_skills - current_skills
                    
                    if new_skills:
                        st.markdown("**New Skills Needed:**")
                        for skill in new_skills:
                            st.markdown(f"- {skill}")
                    
                    # Salary change
                    salary_change = next_role['salary'] - role['salary']
                    salary_change_pct = (salary_change / role['salary']) * 100 if role['salary'] > 0 else 0
                    
                    st.markdown(f"**Salary Change:** {'+' if salary_change >= 0 else ''}{salary_change:,} ({'+' if salary_change_pct >= 0 else ''}{salary_change_pct:.1f}%)")

if __name__ == "__main__":
    main()
