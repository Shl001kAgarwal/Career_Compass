import pandas as pd
import numpy as np

# Global variable to store career skills dataset
CAREER_SKILL_DATASET = []

def load_career_skill_dataset():
    """
    Load career skills dataset
    
    In a real application, this would load data from an API or database
    For this implementation, we'll create a sample dataset
    """
    global CAREER_SKILL_DATASET
    
    # Generate sample career skills dataset
    CAREER_SKILL_DATASET = create_sample_career_skill_dataset()
    
    return True

def get_career_skill_dataset():
    """
    Get the career skills dataset
    
    Returns:
        list: List of career skill entries (each a dict with company, job title, and skills)
    """
    if not CAREER_SKILL_DATASET:
        load_career_skill_dataset()
    
    return CAREER_SKILL_DATASET

def create_sample_career_skill_dataset():
    """
    Create a sample career-skill dataset for ML training
    
    Returns:
        list: List of career entries with skills
    """
    # Sample dataset with company, job title, and required skills
    return [
        # Software Developer entries
        {"company": "Microsoft", "job_title": "Software Developer", "skills": ["python", "java", "c#", "azure", "sql", "git", "algorithms", "problem solving"]},
        {"company": "Google", "job_title": "Software Developer", "skills": ["python", "go", "c++", "kubernetes", "cloud computing", "algorithms", "distributed systems"]},
        {"company": "Amazon", "job_title": "Software Developer", "skills": ["java", "aws", "microservices", "algorithms", "rest apis", "nosql", "agile"]},
        {"company": "Facebook", "job_title": "Software Developer", "skills": ["python", "react", "javascript", "django", "data structures", "system design", "scalability"]},
        {"company": "Apple", "job_title": "Software Developer", "skills": ["swift", "objective-c", "ios", "xcode", "mobile development", "ui/ux", "cocoa"]},
        {"company": "Netflix", "job_title": "Software Developer", "skills": ["java", "javascript", "microservices", "aws", "streaming technologies", "algorithms"]},
        {"company": "IBM", "job_title": "Software Developer", "skills": ["java", "spring", "cloud computing", "microservices", "rest apis", "sql", "docker"]},
        {"company": "Oracle", "job_title": "Software Developer", "skills": ["java", "oracle db", "sql", "pl/sql", "rest apis", "spring", "microservices"]},
        
        # Data Scientist entries
        {"company": "Google", "job_title": "Data Scientist", "skills": ["python", "tensorflow", "machine learning", "statistics", "sql", "data visualization", "nlp"]},
        {"company": "Facebook", "job_title": "Data Scientist", "skills": ["python", "r", "sql", "machine learning", "statistics", "a/b testing", "data visualization"]},
        {"company": "Amazon", "job_title": "Data Scientist", "skills": ["python", "machine learning", "statistics", "aws", "sql", "data modeling", "algorithms"]},
        {"company": "Microsoft", "job_title": "Data Scientist", "skills": ["python", "azure", "machine learning", "deep learning", "sql", "power bi", "statistics"]},
        {"company": "Netflix", "job_title": "Data Scientist", "skills": ["python", "sql", "recommendation systems", "a/b testing", "statistics", "machine learning"]},
        {"company": "IBM", "job_title": "Data Scientist", "skills": ["python", "machine learning", "watson", "statistics", "data visualization", "sql", "cloud computing"]},
        {"company": "Uber", "job_title": "Data Scientist", "skills": ["python", "sql", "machine learning", "statistics", "optimization", "geospatial analysis"]},
        {"company": "Airbnb", "job_title": "Data Scientist", "skills": ["python", "r", "sql", "machine learning", "statistics", "experimentation", "data visualization"]},
        
        # Computer and Information Systems Manager entries
        {"company": "IBM", "job_title": "Computer and Information Systems Manager", "skills": ["project management", "leadership", "cloud computing", "budgeting", "it strategy", "communication"]},
        {"company": "Microsoft", "job_title": "Computer and Information Systems Manager", "skills": ["project management", "azure", "team leadership", "budgeting", "strategic planning", "vendor management"]},
        {"company": "Deloitte", "job_title": "Computer and Information Systems Manager", "skills": ["it governance", "project management", "consulting", "team leadership", "client management", "risk management"]},
        {"company": "Accenture", "job_title": "Computer and Information Systems Manager", "skills": ["project management", "it strategy", "team leadership", "consulting", "digital transformation", "change management"]},
        {"company": "Oracle", "job_title": "Computer and Information Systems Manager", "skills": ["project management", "oracle technologies", "leadership", "budgeting", "vendor management", "strategic planning"]},
        {"company": "Cognizant", "job_title": "Computer and Information Systems Manager", "skills": ["project management", "leadership", "it service management", "outsourcing", "client management", "it operations"]},
        {"company": "Cisco", "job_title": "Computer and Information Systems Manager", "skills": ["network management", "leadership", "cybersecurity", "project management", "strategic planning", "team building"]},
        {"company": "SAP", "job_title": "Computer and Information Systems Manager", "skills": ["erp systems", "sap technologies", "project management", "leadership", "business process optimization", "strategic planning"]},
        
        # Marketing Manager entries
        {"company": "Procter & Gamble", "job_title": "Marketing Manager", "skills": ["brand management", "market research", "digital marketing", "strategic planning", "communication", "leadership"]},
        {"company": "Unilever", "job_title": "Marketing Manager", "skills": ["brand management", "consumer behavior", "strategic planning", "product marketing", "digital marketing", "team leadership"]},
        {"company": "Coca-Cola", "job_title": "Marketing Manager", "skills": ["brand management", "campaign management", "market analysis", "strategic planning", "digital marketing", "consumer insights"]},
        {"company": "PepsiCo", "job_title": "Marketing Manager", "skills": ["brand management", "consumer insights", "strategic planning", "product marketing", "advertising", "leadership"]},
        {"company": "Nike", "job_title": "Marketing Manager", "skills": ["brand management", "campaign development", "social media marketing", "sports marketing", "leadership", "consumer behavior"]},
        {"company": "L'Oréal", "job_title": "Marketing Manager", "skills": ["brand management", "product marketing", "market research", "advertising", "leadership", "marketing strategy"]},
        {"company": "Amazon", "job_title": "Marketing Manager", "skills": ["digital marketing", "seo", "sem", "marketing analytics", "strategic planning", "leadership", "e-commerce marketing"]},
        {"company": "Johnson & Johnson", "job_title": "Marketing Manager", "skills": ["brand management", "healthcare marketing", "market research", "strategic planning", "leadership", "new product development"]},
        
        # Market Research Analyst entries
        {"company": "Nielsen", "job_title": "Market Research Analyst", "skills": ["data analysis", "market research", "statistics", "survey design", "spss", "report writing", "data visualization"]},
        {"company": "Ipsos", "job_title": "Market Research Analyst", "skills": ["market research", "data analysis", "survey design", "focus groups", "statistics", "report writing", "presentation skills"]},
        {"company": "Kantar", "job_title": "Market Research Analyst", "skills": ["market research", "data analysis", "statistics", "survey design", "qualitative research", "report writing", "presentation skills"]},
        {"company": "Procter & Gamble", "job_title": "Market Research Analyst", "skills": ["consumer research", "data analysis", "market trends", "statistics", "presentation skills", "excel", "product testing"]},
        {"company": "McKinsey & Company", "job_title": "Market Research Analyst", "skills": ["market analysis", "data analytics", "industry research", "business intelligence", "report writing", "excel", "powerpoint"]},
        {"company": "Unilever", "job_title": "Market Research Analyst", "skills": ["consumer research", "data analysis", "market trends", "statistics", "brand performance tracking", "excel", "presentation skills"]},
        {"company": "Boston Consulting Group", "job_title": "Market Research Analyst", "skills": ["market analysis", "data analytics", "industry research", "consulting", "report writing", "excel", "research methods"]},
        {"company": "Google", "job_title": "Market Research Analyst", "skills": ["data analysis", "market research", "statistics", "python", "sql", "data visualization", "survey design"]},
        
        # Accountant entries
        {"company": "Deloitte", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "gaap", "excel", "tax preparation", "quickbooks"]},
        {"company": "PwC", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "tax preparation", "excel", "sap", "financial analysis"]},
        {"company": "EY", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "gaap", "ifrs", "excel", "tax preparation"]},
        {"company": "KPMG", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "tax preparation", "excel", "financial analysis", "risk assessment"]},
        {"company": "Grant Thornton", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "gaap", "tax preparation", "excel", "financial analysis"]},
        {"company": "BDO", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "tax preparation", "gaap", "excel", "client management"]},
        {"company": "RSM", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "tax preparation", "excel", "quickbooks", "client relations"]},
        {"company": "Baker Tilly", "job_title": "Accountant", "skills": ["accounting", "auditing", "financial reporting", "tax preparation", "gaap", "excel", "financial analysis"]},
        
        # Registered Nurse entries
        {"company": "HCA Healthcare", "job_title": "Registered Nurse", "skills": ["patient care", "medication administration", "electronic medical records", "critical thinking", "communication", "teamwork"]},
        {"company": "CommonSpirit Health", "job_title": "Registered Nurse", "skills": ["patient care", "clinical assessment", "medication administration", "electronic medical records", "communication", "teamwork"]},
        {"company": "Ascension", "job_title": "Registered Nurse", "skills": ["patient care", "clinical skills", "medication administration", "electronic medical records", "critical thinking", "patient education"]},
        {"company": "Kaiser Permanente", "job_title": "Registered Nurse", "skills": ["patient care", "clinical assessment", "medication administration", "epic", "communication", "care coordination"]},
        {"company": "Providence", "job_title": "Registered Nurse", "skills": ["patient care", "clinical skills", "medication administration", "electronic medical records", "critical thinking", "teamwork"]},
        {"company": "Tenet Healthcare", "job_title": "Registered Nurse", "skills": ["patient care", "clinical assessment", "medication administration", "electronic medical records", "critical thinking", "time management"]},
        {"company": "Cleveland Clinic", "job_title": "Registered Nurse", "skills": ["patient care", "clinical skills", "medication administration", "epic", "communication", "team collaboration", "patient education"]},
        {"company": "Mayo Clinic", "job_title": "Registered Nurse", "skills": ["patient care", "clinical assessment", "medication administration", "electronic medical records", "critical thinking", "research"]},
        
        # Elementary School Teacher entries
        {"company": "New York City Department of Education", "job_title": "Elementary School Teacher", "skills": ["curriculum development", "classroom management", "lesson planning", "assessment", "communication", "differentiated instruction"]},
        {"company": "Los Angeles Unified School District", "job_title": "Elementary School Teacher", "skills": ["curriculum implementation", "classroom management", "assessment", "technology integration", "communication", "bilingual education"]},
        {"company": "Chicago Public Schools", "job_title": "Elementary School Teacher", "skills": ["curriculum development", "classroom management", "lesson planning", "assessment", "communication", "cultural awareness"]},
        {"company": "Miami-Dade County Public Schools", "job_title": "Elementary School Teacher", "skills": ["curriculum implementation", "classroom management", "lesson planning", "bilingual education", "assessment", "parental communication"]},
        {"company": "Clark County School District", "job_title": "Elementary School Teacher", "skills": ["curriculum development", "classroom management", "assessment", "technology integration", "communication", "team collaboration"]},
        {"company": "Houston Independent School District", "job_title": "Elementary School Teacher", "skills": ["curriculum implementation", "classroom management", "assessment", "lesson planning", "communication", "cultural awareness"]},
        {"company": "Broward County Public Schools", "job_title": "Elementary School Teacher", "skills": ["curriculum development", "classroom management", "lesson planning", "assessment", "technology integration", "communication"]},
        {"company": "Hawaii Department of Education", "job_title": "Elementary School Teacher", "skills": ["curriculum implementation", "classroom management", "assessment", "cultural awareness", "communication", "differentiated instruction"]},
        
        # Civil Engineer entries
        {"company": "AECOM", "job_title": "Civil Engineer", "skills": ["autocad", "civil 3d", "project management", "structural analysis", "construction management", "technical writing"]},
        {"company": "Jacobs", "job_title": "Civil Engineer", "skills": ["autocad", "civil 3d", "project management", "structural analysis", "geotechnical engineering", "environmental compliance"]},
        {"company": "Fluor", "job_title": "Civil Engineer", "skills": ["autocad", "project management", "structural analysis", "construction management", "cost estimation", "technical writing"]},
        {"company": "Bechtel", "job_title": "Civil Engineer", "skills": ["autocad", "project management", "structural analysis", "construction management", "cost estimation", "quality control"]},
        {"company": "Kiewit", "job_title": "Civil Engineer", "skills": ["autocad", "project management", "construction management", "structural analysis", "cost estimation", "contract administration"]},
        {"company": "HDR", "job_title": "Civil Engineer", "skills": ["autocad", "civil 3d", "project management", "structural analysis", "hydraulic modeling", "environmental engineering"]},
        {"company": "WSP", "job_title": "Civil Engineer", "skills": ["autocad", "project management", "structural analysis", "transportation engineering", "environmental compliance", "technical writing"]},
        {"company": "Stantec", "job_title": "Civil Engineer", "skills": ["autocad", "civil 3d", "project management", "structural analysis", "environmental engineering", "land development"]}
    ]