import re
import PyPDF2
import io
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import streamlit as st

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is not available, use a simpler approach with NLTK
    nlp = None

def parse_resume(uploaded_file):
    """
    Parse a resume file and extract relevant information
    
    Args:
        uploaded_file: The uploaded resume file (PDF or text)
        
    Returns:
        dict: A dictionary containing parsed resume data
    """
    content = ""
    
    try:
        # Handle PDF files
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page_num in range(len(reader.pages)):
                content += reader.pages[page_num].extract_text()
        
        # Handle text files
        elif uploaded_file.type == "text/plain":
            content = uploaded_file.getvalue().decode("utf-8")
            
        else:
            return {"error": "Unsupported file format. Please upload a PDF or text file."}
    
    except Exception as e:
        return {"error": f"Error parsing resume: {str(e)}"}
    
    # Process the extracted content
    resume_data = extract_resume_data(content)
    
    return resume_data

def extract_resume_data(text):
    """
    Extract structured data from resume text
    
    Args:
        text: The text content of the resume
        
    Returns:
        dict: Structured resume data
    """
    # Basic cleaning
    text = text.replace('\n', ' ').replace('\r', '').strip()
    text = re.sub(' +', ' ', text)
    
    result = {
        "raw_text": text,
        "contact_info": extract_contact_info(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "skills": extract_skills(text)
    }
    
    return result

def extract_contact_info(text):
    """Extract contact information from resume text"""
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, text)
    email = email_matches[0] if email_matches else ""
    
    # Extract phone number
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    phone_matches = re.findall(phone_pattern, text)
    phone = ''.join(''.join(tup) for tup in phone_matches[:1]) if phone_matches else ""
    
    # Extract LinkedIn (simplified)
    linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9_-]+'
    linkedin_matches = re.findall(linkedin_pattern, text)
    linkedin = linkedin_matches[0] if linkedin_matches else ""
    
    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin
    }

def extract_education(text):
    """Extract education information from resume text"""
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'university', 
                          'college', 'school', 'institute', 'certification', 'b.tech', 
                          'm.tech', 'b.e.', 'm.e.', 'b.sc', 'm.sc', 'b.a.', 'm.a.']
    
    education_data = []
    
    # Simple detection based on keywords
    sentences = re.split(r'[.\n]', text)
    for sentence in sentences:
        sentence = sentence.lower().strip()
        if any(keyword in sentence for keyword in education_keywords):
            education_data.append(sentence)
    
    return education_data

def extract_experience(text):
    """Extract work experience from resume text"""
    experience_markers = ['experience', 'employment', 'work history', 'job history', 
                          'professional experience', 'career']
    
    experience_data = []
    
    # Simple parsing based on sections
    text_lower = text.lower()
    for marker in experience_markers:
        if marker in text_lower:
            # Find the section
            pattern = re.compile(f"{marker}.*?\n", re.IGNORECASE)
            matches = pattern.finditer(text)
            for match in matches:
                start_idx = match.end()
                
                # Find the end of the section (next heading or end of text)
                next_heading = re.search(r'\n[A-Z][A-Z\s]+\n', text[start_idx:])
                if next_heading:
                    end_idx = start_idx + next_heading.start()
                else:
                    end_idx = len(text)
                
                experience_section = text[start_idx:end_idx].strip()
                experience_data.append(experience_section)
    
    return experience_data

def extract_skills(text):
    """Extract skills from resume text"""
    # Common skill keywords
    technical_skills = [
        'python', 'java', 'javascript', 'c++', 'c#', 'r', 'sql', 'nosql', 'django',
        'flask', 'react', 'angular', 'vue', 'node', 'express', 'php', 'ruby', 'perl',
        'html', 'css', 'sass', 'bootstrap', 'jquery', 'ajax', 'json', 'xml', 'rest',
        'api', 'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'jenkins',
        'ci/cd', 'git', 'svn', 'jira', 'agile', 'scrum', 'waterfall', 'sdlc',
        'data analysis', 'data science', 'machine learning', 'deep learning', 'ai',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy',
        'matplotlib', 'seaborn', 'tableau', 'power bi', 'excel', 'word', 'powerpoint',
        'mysql', 'postgresql', 'mongodb', 'oracle', 'redis', 'elasticsearch',
        'hadoop', 'spark', 'kafka', 'scala', 'swift', 'objective-c', 'kotlin',
        'flutter', 'react native', 'mobile development', 'web development', 
        'data engineering', 'devops', 'sysadmin', 'network', 'security', 'blockchain'
    ]
    
    soft_skills = [
        'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
        'creativity', 'time management', 'organization', 'adaptability', 'flexibility',
        'negotiation', 'persuasion', 'presentation', 'analytical', 'research', 'planning',
        'decision making', 'emotional intelligence', 'conflict resolution', 'mentoring',
        'coaching', 'collaboration', 'interpersonal', 'multitasking', 'attention to detail',
        'customer service', 'client relations', 'project management', 'team building',
        'strategic thinking', 'innovation', 'motivation', 'self-starter', 'independent',
        'proactive', 'initiative', 'stress management', 'patience', 'persistence', 'resilience'
    ]
    
    all_skills = technical_skills + soft_skills
    
    # Extract skills
    text_lower = text.lower()
    found_skills = []
    
    for skill in all_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill)
    
    # Use spaCy for entity extraction if available
    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "GPE"] and len(ent.text) > 2:
                found_skills.append(ent.text.lower())
                
    # Remove duplicates and sort
    found_skills = sorted(list(set(found_skills)))
    
    # Categorize skills
    categorized_skills = {
        "technical": [skill for skill in found_skills if skill in technical_skills],
        "soft": [skill for skill in found_skills if skill in soft_skills],
    }
    
    return categorized_skills
