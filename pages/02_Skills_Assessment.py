import streamlit as st
from utils.resume_parser import extract_skills

st.set_page_config(
    page_title="Skills Assessment - Career Compass",
    page_icon="🛠️",
    layout="wide"
)

def main():
    st.title("🛠️ Skills Assessment")
    st.write("Review, edit, and add to your skills to improve your career recommendations.")
    
    # Initialize skills in session state if not present
    if "skills" not in st.session_state:
        st.session_state.skills = {"technical": [], "soft": []}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Technical Skills Section
        st.subheader("Technical Skills")
        st.write("These are specific, job-related skills that demonstrate your expertise in particular technologies, tools, or methodologies.")
        
        # Display existing technical skills with delete option
        if "technical" in st.session_state.skills and st.session_state.skills["technical"]:
            tech_skills = st.session_state.skills["technical"]
            
            # Create a container for the skills pills
            tech_skills_container = st.container()
            
            # Create delete buttons for each skill
            deleted_tech_skills = []
            for i, skill in enumerate(tech_skills):
                if st.checkbox(f"Remove {skill}", key=f"del_tech_{i}", value=False):
                    deleted_tech_skills.append(skill)
            
            # Remove deleted skills
            for skill in deleted_tech_skills:
                st.session_state.skills["technical"].remove(skill)
            
            # Display remaining skills as pills
            with tech_skills_container:
                if st.session_state.skills["technical"]:
                    st.write("Your technical skills:")
                    html_skills = ""
                    for skill in st.session_state.skills["technical"]:
                        html_skills += f'<span style="background-color:#1E88E5;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
                    st.markdown(html_skills, unsafe_allow_html=True)
                else:
                    st.info("No technical skills selected yet.")
        else:
            st.info("No technical skills identified yet. Add some below.")
        
        # Add new technical skills
        new_tech_skill = st.text_input("Add a new technical skill:", key="new_tech_skill")
        if st.button("Add Technical Skill"):
            if new_tech_skill and new_tech_skill.strip():
                if "technical" not in st.session_state.skills:
                    st.session_state.skills["technical"] = []
                
                # Add the skill if not already in the list
                if new_tech_skill.lower() not in [skill.lower() for skill in st.session_state.skills["technical"]]:
                    st.session_state.skills["technical"].append(new_tech_skill)
                    st.success(f"Added {new_tech_skill} to your technical skills!")
                else:
                    st.warning(f"{new_tech_skill} is already in your skills list.")
                
                st._rerun()
        
        # Suggest common skills
        st.markdown("### Common Technical Skills")
        common_tech_skills = [
            "Python", "Java", "JavaScript", "C++", "SQL", "Data Analysis", 
            "Machine Learning", "AWS", "Azure", "React", "Node.js", "HTML/CSS",
            "Git", "Docker", "Kubernetes", "Excel", "Power BI", "Tableau",
            "TensorFlow", "PyTorch", "NLP", "Data Visualization", "REST APIs",
            "DevOps", "Agile Methodology", "Scrum", "Testing", "CI/CD"
        ]
        
        # Display common skills as clickable buttons
        common_tech_cols = st.columns(4)
        for i, skill in enumerate(common_tech_skills):
            col_idx = i % 4
            with common_tech_cols[col_idx]:
                disabled = skill in st.session_state.skills.get("technical", [])
                if st.button(skill, disabled=disabled, key=f"common_tech_{i}"):
                    if "technical" not in st.session_state.skills:
                        st.session_state.skills["technical"] = []
                    st.session_state.skills["technical"].append(skill)
                    st._rerun()
        
        # Soft Skills Section
        st.subheader("Soft Skills")
        st.write("These are interpersonal and transferable skills that are valuable across various jobs and industries.")
        
        # Display existing soft skills with delete option
        if "soft" in st.session_state.skills and st.session_state.skills["soft"]:
            soft_skills = st.session_state.skills["soft"]
            
            # Create a container for the skills pills
            soft_skills_container = st.container()
            
            # Create delete buttons for each skill
            deleted_soft_skills = []
            for i, skill in enumerate(soft_skills):
                if st.checkbox(f"Remove {skill}", key=f"del_soft_{i}", value=False):
                    deleted_soft_skills.append(skill)
            
            # Remove deleted skills
            for skill in deleted_soft_skills:
                st.session_state.skills["soft"].remove(skill)
            
            # Display remaining skills as pills
            with soft_skills_container:
                if st.session_state.skills["soft"]:
                    st.write("Your soft skills:")
                    html_skills = ""
                    for skill in st.session_state.skills["soft"]:
                        html_skills += f'<span style="background-color:#43A047;color:white;padding:4px 8px;margin:4px;border-radius:12px;display:inline-block">{skill}</span>'
                    st.markdown(html_skills, unsafe_allow_html=True)
                else:
                    st.info("No soft skills selected yet.")
        else:
            st.info("No soft skills identified yet. Add some below.")
        
        # Add new soft skills
        new_soft_skill = st.text_input("Add a new soft skill:", key="new_soft_skill")
        if st.button("Add Soft Skill"):
            if new_soft_skill and new_soft_skill.strip():
                if "soft" not in st.session_state.skills:
                    st.session_state.skills["soft"] = []
                
                # Add the skill if not already in the list
                if new_soft_skill.lower() not in [skill.lower() for skill in st.session_state.skills["soft"]]:
                    st.session_state.skills["soft"].append(new_soft_skill)
                    st.success(f"Added {new_soft_skill} to your soft skills!")
                else:
                    st.warning(f"{new_soft_skill} is already in your skills list.")
                
                st._rerun()
        
        # Suggest common soft skills
        st.markdown("### Common Soft Skills")
        common_soft_skills = [
            "Communication", "Teamwork", "Problem Solving", "Leadership", 
            "Time Management", "Critical Thinking", "Adaptability", "Creativity",
            "Attention to Detail", "Analytical Thinking", "Decision Making", 
            "Emotional Intelligence", "Conflict Resolution", "Negotiation",
            "Presentation Skills", "Writing", "Customer Service", "Mentoring"
        ]
        
        # Display common skills as clickable buttons
        common_soft_cols = st.columns(4)
        for i, skill in enumerate(common_soft_skills):
            col_idx = i % 4
            with common_soft_cols[col_idx]:
                disabled = skill in st.session_state.skills.get("soft", [])
                if st.button(skill, disabled=disabled, key=f"common_soft_{i}"):
                    if "soft" not in st.session_state.skills:
                        st.session_state.skills["soft"] = []
                    st.session_state.skills["soft"].append(skill)
                    st._rerun()
        
        # Next steps and navigation
        st.markdown("---")
        if len(st.session_state.skills.get("technical", [])) + len(st.session_state.skills.get("soft", [])) > 0:
            st.success("Great job! You've identified your skills. Now let's assess your personality and interests.")
            if st.button("Continue to Personality Assessment"):
                # Navigate to next page
                st._rerun()
        else:
            st.warning("Please add at least one skill before continuing.")
    
    with col2:
        st.image("https://pixabay.com/get/g185b8d288b58cd78b0eacefafa2b0946a15f1f42b6ddc771de456506b3d7146aade041355e0cd708fefcaa650080d2a63fffde29788b44d195f2f34167e8297f_1280.jpg", caption="Skills Development")
        
        st.markdown("""
        ### Why Skills Matter
        
        Your skills profile plays a crucial role in determining suitable career paths. The more accurately you identify your skills, the better your recommendations will be.
        
        #### Technical vs. Soft Skills
        
        **Technical Skills** are specific to a profession:
        - Programming languages
        - Data analysis
        - Software proficiency
        - Industry certifications
        
        **Soft Skills** are transferable across careers:
        - Communication
        - Leadership
        - Problem-solving
        - Teamwork
        
        Both are equally important in today's job market!
        """)
        
        # Tips for skill assessment
        st.markdown("""
        ### Tips for Skill Assessment
        
        1. **Be honest** about your skill levels
        2. **Include skills** from personal projects
        3. **Consider transferable skills** from previous roles
        4. **Don't underestimate** soft skills
        5. **Add skills** you're currently learning
        """)

if __name__ == "__main__":
    main()
