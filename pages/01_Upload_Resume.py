import streamlit as st
import pandas as pd
import base64
from utils.resume_parser import parse_resume

st.set_page_config(
    page_title="Upload Resume - Career Compass",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 Upload Your Resume")
    st.write("Upload your resume to get started with personalized career recommendations.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Why Upload Your Resume?
        
        Your resume contains valuable information about your skills, experience, and education that helps us:
        
        - Identify your current skill set
        - Understand your work experience
        - Analyze your educational background
        - Find relevant career matches
        - Determine skill gaps for your target roles
        
        ### Supported Formats
        
        We currently support **PDF** and **TXT** resume files.
        """)
        
        # File uploader
        uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "txt"])
        
        if uploaded_file is not None:
            st.success("File successfully uploaded!")
            
            # Parse the resume
            with st.spinner("Analyzing your resume..."):
                resume_data = parse_resume(uploaded_file)
                
                if "error" in resume_data:
                    st.error(resume_data["error"])
                else:
                    # Save to session state
                    st.session_state.resume_data = resume_data
                    
                    # Display confirmation
                    st.success("Resume successfully parsed! Here's what we found:")
                    
                    # Extract basic info
                    contact_info = resume_data.get("contact_info", {})
                    skills = resume_data.get("skills", {})
                    
                    # Display skills extracted
                    st.subheader("Skills Identified")
                    
                    technical_skills = skills.get("technical", [])
                    soft_skills = skills.get("soft", [])
                    
                    if technical_skills:
                        st.write("**Technical Skills:**")
                        st.write(", ".join(technical_skills))
                    
                    if soft_skills:
                        st.write("**Soft Skills:**")
                        st.write(", ".join(soft_skills))
                    
                    if not technical_skills and not soft_skills:
                        st.info("No specific skills identified. You'll be able to add them manually in the next step.")
                    
                    # Save skills to session state
                    st.session_state.skills = skills
                    
                    # Next steps
                    st.markdown("""
                    ### Next Steps
                    
                    1. Proceed to the **Skills Assessment** page to review and refine your skills
                    2. Take a **Personality Assessment** to help us match you with suitable careers
                    3. Explore your personalized **Career Recommendations**
                    """)
                    
                    # Navigation button
                    st.button("Continue to Skills Assessment", on_click=lambda: st.session_state.update({"page": "skills_assessment"}))
    
    with col2:
        st.image("https://pixabay.com/get/g9e0e22cbd92f6800fd49c6f02a676de532002b0f8e715a449fc3896cd3e8a364fa309073a88c62b524c73a2755edb7c29454ffb933a2f904265b1cc3b6b1e603_1280.jpg", caption="Career professionals")
        
        st.markdown("""
        ### Resume Tips
        
        For best results:
        
        ✅ Include detailed skills section  
        ✅ List technologies & tools  
        ✅ Quantify achievements  
        ✅ Include education details  
        ✅ Mention certifications  
        
        ---
        
        If you don't have a resume ready, you can proceed to the **Skills Assessment** page and enter your information manually.
        """)
        
        # Alternative navigation
        if st.button("Skip resume upload"):
            st.session_state.resume_data = None
            st.session_state.skills = {"technical": [], "soft": []}
            st._rerun()

if __name__ == "__main__":
    main()
