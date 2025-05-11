import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Personality Assessment - Career Compass",
    page_icon="🧠",
    layout="wide"
)

def main():
    st.title("🧠 Personality Assessment")
    st.write("Complete this assessment to help us match you with careers that align with your personality and interests.")
    
    # Initialize personality results in session state if not present
    if "personality_results" not in st.session_state:
        st.session_state.personality_results = {}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # RIASEC Assessment - Holland Occupational Themes
        st.header("RIASEC Assessment")
        st.write("""
        The RIASEC model identifies six personality types that influence career preferences:
        
        - **Realistic**: Practical, hands-on problem solvers
        - **Investigative**: Analytical, intellectual, scientific
        - **Artistic**: Creative, original, independent
        - **Social**: Empathetic, cooperative, supportive
        - **Enterprising**: Persuasive, goal-oriented leaders
        - **Conventional**: Detail-oriented, organized, methodical
        """)
        
        # Check if RIASEC assessment is already completed
        if "riasec" in st.session_state.personality_results:
            display_riasec_results()
            
            # Option to retake the assessment
            if st.button("Retake RIASEC Assessment"):
                # Remove the RIASEC results to retake
                if "riasec" in st.session_state.personality_results:
                    del st.session_state.personality_results["riasec"]
                st._rerun()
        else:
            # Display the RIASEC assessment questions
            st.subheader("Rate how much you enjoy the following activities:")
            st.write("(1 = Strongly Dislike, 5 = Strongly Enjoy)")
            
            # Create questions for each RIASEC dimension
            riasec_questions = create_riasec_questions()
            
            # Create a form for the assessment
            with st.form("riasec_form"):
                responses = {}
                
                # Group questions by RIASEC dimension for organization
                for dimension, questions in riasec_questions.items():
                    st.subheader(f"{dimension} Questions")
                    
                    for i, question in enumerate(questions):
                        question_key = f"{dimension.lower()}_{i}"
                        responses[question_key] = st.slider(
                            question, 
                            min_value=1, 
                            max_value=5, 
                            value=3, 
                            key=question_key
                        )
                
                # Submit button
                submit_button = st.form_submit_button("Submit Assessment")
                
                if submit_button:
                    # Calculate RIASEC scores
                    riasec_scores = calculate_riasec_scores(responses, riasec_questions)
                    
                    # Save results to session state
                    if "personality_results" not in st.session_state:
                        st.session_state.personality_results = {}
                    
                    st.session_state.personality_results["riasec"] = riasec_scores
                    
                    # Refresh to display results
                    st._rerun()
        
        # Learning Style Assessment (simplified)
        st.markdown("---")
        st.header("Learning Style Assessment")
        
        # Check if learning style assessment is already completed
        if "learning_style" in st.session_state.personality_results:
            st.subheader("Your Learning Style")
            learning_style = st.session_state.personality_results["learning_style"]
            
            st.info(f"Your primary learning style is: **{learning_style}**")
            
            # Show learning style description
            learning_style_descriptions = {
                "visual": "You learn best through visual aids like images, diagrams, and videos. Visual learners benefit from seeing information presented graphically.",
                "auditory": "You learn best by hearing information. Auditory learners benefit from lectures, discussions, and audio materials.",
                "reading/writing": "You learn best through written words. You prefer text-based materials like books, articles, and written notes.",
                "kinesthetic": "You learn best through hands-on experiences. Kinesthetic learners benefit from practical activities and applying concepts."
            }
            
            st.write(learning_style_descriptions.get(learning_style.lower(), ""))
            
            # Option to retake the assessment
            if st.button("Retake Learning Style Assessment"):
                # Remove the learning style results to retake
                if "learning_style" in st.session_state.personality_results:
                    del st.session_state.personality_results["learning_style"]
                st._rerun()
        else:
            # Display the learning style assessment questions
            st.subheader("How do you prefer to learn new information?")
            
            with st.form("learning_style_form"):
                # Learning style questions
                visual_score = st.slider(
                    "I prefer to learn using charts, diagrams, and visual aids", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                auditory_score = st.slider(
                    "I prefer to learn by listening to explanations and discussions", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                reading_score = st.slider(
                    "I prefer to learn by reading and writing information", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                kinesthetic_score = st.slider(
                    "I prefer to learn through hands-on activities and practice", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                # Submit button
                submit_button = st.form_submit_button("Submit Learning Style")
                
                if submit_button:
                    # Determine primary learning style
                    styles = {
                        "Visual": visual_score,
                        "Auditory": auditory_score,
                        "Reading/Writing": reading_score,
                        "Kinesthetic": kinesthetic_score
                    }
                    
                    primary_style = max(styles.items(), key=lambda x: x[1])[0]
                    
                    # Save results to session state
                    if "personality_results" not in st.session_state:
                        st.session_state.personality_results = {}
                    
                    st.session_state.personality_results["learning_style"] = primary_style
                    
                    # Refresh to display results
                    st._rerun()
        
        # Work Environment Preferences
        st.markdown("---")
        st.header("Work Environment Preferences")
        
        # Check if work environment assessment is already completed
        if "work_environment" in st.session_state.personality_results:
            st.subheader("Your Work Environment Preferences")
            work_prefs = st.session_state.personality_results["work_environment"]
            
            # Create a radar chart for work preferences
            categories = list(work_prefs.keys())
            values = list(work_prefs.values())
            
            # Close the polygon by appending the first value to the end
            values.append(values[0])
            categories.append(categories[0])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Work Preferences'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=False,
                title="Work Environment Preferences"
            )
            
            st.plotly_chart(fig)
            
            # Interpret results
            highest_pref = max(work_prefs.items(), key=lambda x: x[1])[0]
            lowest_pref = min(work_prefs.items(), key=lambda x: x[1])[0]
            
            st.write(f"You show a strong preference for **{highest_pref}** work environments.")
            st.write(f"You may be less comfortable in **{lowest_pref}** work settings.")
            
            # Option to retake the assessment
            if st.button("Retake Work Environment Assessment"):
                # Remove the work environment results to retake
                if "work_environment" in st.session_state.personality_results:
                    del st.session_state.personality_results["work_environment"]
                st._rerun()
        else:
            # Display the work environment assessment questions
            st.subheader("Rate your preference for each work environment:")
            st.write("(1 = Strongly Dislike, 5 = Strongly Prefer)")
            
            with st.form("work_environment_form"):
                # Work environment questions
                collaborative = st.slider(
                    "Collaborative environments where teamwork is essential", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                independent = st.slider(
                    "Independent work with minimal supervision", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                structured = st.slider(
                    "Structured environments with clear processes and rules", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                flexible = st.slider(
                    "Flexible and adaptable environments with changing priorities", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                competitive = st.slider(
                    "Competitive environments with performance incentives", 
                    min_value=1, 
                    max_value=5, 
                    value=3
                )
                
                # Submit button
                submit_button = st.form_submit_button("Submit Work Preferences")
                
                if submit_button:
                    # Save work environment preferences
                    work_preferences = {
                        "Collaborative": collaborative,
                        "Independent": independent,
                        "Structured": structured,
                        "Flexible": flexible,
                        "Competitive": competitive
                    }
                    
                    # Save results to session state
                    if "personality_results" not in st.session_state:
                        st.session_state.personality_results = {}
                    
                    st.session_state.personality_results["work_environment"] = work_preferences
                    
                    # Refresh to display results
                    st._rerun()
        
        # Navigation footer
        st.markdown("---")
        if all(k in st.session_state.personality_results for k in ["riasec", "learning_style", "work_environment"]):
            st.success("Great job! You've completed all personality assessments.")
            if st.button("Continue to Career Recommendations"):
                # Navigate to next page
                st._rerun()
    
    with col2:
        st.image("https://pixabay.com/get/g06da8e6bc34e3ae8d5e45ddf920d033a6c7b690988fc5a183b66396fc0284cf59b1672104b38a5d29d25472ad2e5787a0c2e29a1e7a54c32df043a3d2f8845f3_1280.jpg", caption="Personality Assessment")
        
        st.markdown("""
        ### Why Personality Matters
        
        Your personality traits and preferences significantly impact job satisfaction and career success. This assessment helps us:
        
        - Match you with careers that align with your natural tendencies
        - Identify work environments where you're likely to thrive
        - Suggest career paths that match your interests
        - Recommend learning approaches based on your style
        
        ### How This Improves Your Recommendations
        
        By considering both your skills AND personality, we can provide:
        
        - More holistic career suggestions
        - Better cultural fit predictions
        - Personalized development paths
        - Higher likelihood of job satisfaction
        """)
        
        # Show completion status
        st.markdown("### Assessment Progress")
        completed_assessments = sum(1 for k in ["riasec", "learning_style", "work_environment"] if k in st.session_state.personality_results)
        progress_percentage = completed_assessments / 3 * 100
        
        st.progress(progress_percentage / 100)
        st.write(f"Completed: {completed_assessments}/3 assessments ({int(progress_percentage)}%)")

def create_riasec_questions():
    """Create questions for the RIASEC assessment"""
    return {
        "Realistic": [
            "Building things with my hands",
            "Working outdoors",
            "Operating machinery or equipment",
            "Working with plants or animals",
            "Repairing electronic devices"
        ],
        "Investigative": [
            "Solving complex problems",
            "Conducting research",
            "Analyzing data and information",
            "Exploring scientific theories",
            "Understanding how things work"
        ],
        "Artistic": [
            "Creating artwork",
            "Writing stories or poetry",
            "Playing musical instruments",
            "Designing new things",
            "Coming up with original ideas"
        ],
        "Social": [
            "Teaching or training others",
            "Helping people with their problems",
            "Working as part of a team",
            "Counseling or providing guidance",
            "Volunteer work in the community"
        ],
        "Enterprising": [
            "Starting a business",
            "Leading a team or project",
            "Persuading others",
            "Making decisions that affect others",
            "Negotiating agreements"
        ],
        "Conventional": [
            "Organizing files or data",
            "Following detailed instructions",
            "Working with numbers",
            "Creating schedules or systems",
            "Attention to detail"
        ]
    }

def calculate_riasec_scores(responses, riasec_questions):
    """Calculate RIASEC scores from questionnaire responses"""
    riasec_scores = {}
    
    # Calculate average score for each dimension
    for dimension, questions in riasec_questions.items():
        dimension_scores = []
        
        for i in range(len(questions)):
            question_key = f"{dimension.lower()}_{i}"
            if question_key in responses:
                dimension_scores.append(responses[question_key])
        
        # Calculate average score for this dimension
        if dimension_scores:
            avg_score = sum(dimension_scores) / len(dimension_scores)
            # Convert to 0-100 scale
            riasec_scores[dimension] = int(avg_score * 20)
    
    return riasec_scores

def display_riasec_results():
    """Display RIASEC assessment results"""
    riasec_scores = st.session_state.personality_results["riasec"]
    
    st.subheader("Your RIASEC Profile")
    
    # Create radar chart for RIASEC results
    categories = list(riasec_scores.keys())
    values = list(riasec_scores.values())
    
    # Close the polygon by appending the first value to the end
    values.append(values[0])
    categories.append(categories[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='RIASEC Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="RIASEC Personality Profile"
    )
    
    st.plotly_chart(fig)
    
    # Identify top RIASEC types
    sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    top_types = sorted_types[:3]
    
    st.write("### Your Top RIASEC Types:")
    
    for type_name, score in top_types:
        st.write(f"**{type_name} ({score}%)**: {get_riasec_description(type_name)}")
    
    # Career guidance based on top type
    st.subheader("What This Means For Your Career")
    st.write(get_riasec_career_guidance(top_types[0][0]))

def get_riasec_description(riasec_type):
    """Get description for a RIASEC type"""
    descriptions = {
        "Realistic": "You are practical, hands-on problem solver who enjoys working with tools, machines, plants, or animals.",
        "Investigative": "You are analytical, intellectual, and scientific, enjoying research, investigation, and understanding complex problems.",
        "Artistic": "You are creative, original, and independent, preferring unstructured environments where you can express your creativity.",
        "Social": "You are empathetic, cooperative, and supportive, enjoying helping, teaching, counseling, or providing service to others.",
        "Enterprising": "You are persuasive, goal-oriented, and leadership-focused, enjoying influencing, leading, and managing for organizational goals.",
        "Conventional": "You are detail-oriented, organized, and methodical, preferring structured environments with clear rules and procedures."
    }
    
    return descriptions.get(riasec_type, "")

def get_riasec_career_guidance(riasec_type):
    """Get career guidance based on top RIASEC type"""
    guidance = {
        "Realistic": "You tend to thrive in careers that involve practical, hands-on work and tangible results. Consider roles in engineering, construction, technical fields, agriculture, or trades where you can apply your practical skills.",
        "Investigative": "You're well-suited for careers that involve analytical thinking, research, and intellectual challenges. Consider roles in science, research, data analysis, medicine, or technology where you can solve complex problems.",
        "Artistic": "You're likely to excel in careers that allow for self-expression, creativity, and working in unstructured environments. Consider roles in design, writing, performing arts, digital media, or creative services.",
        "Social": "You're naturally drawn to careers focused on helping, teaching, or providing service to others. Consider roles in education, healthcare, counseling, human resources, or community services where you can support others' development.",
        "Enterprising": "You're well-matched with careers that involve leadership, persuasion, and achieving organizational goals. Consider roles in management, sales, entrepreneurship, law, or politics where you can lead and influence others.",
        "Conventional": "You're suited for careers that involve organization, data management, and working within clear systems. Consider roles in accounting, administration, logistics, quality assurance, or financial services where attention to detail is valued."
    }
    
    return guidance.get(riasec_type, "")

if __name__ == "__main__":
    main()
