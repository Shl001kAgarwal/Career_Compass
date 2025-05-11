import pandas as pd
import numpy as np
import json
import os
import streamlit as st

# This file contains O*NET occupational data and related functions

# Global variables to store O*NET data
ONET_OCCUPATIONS = []
ONET_SKILLS = {}
ONET_ABILITIES = {}
ONET_KNOWLEDGE = {}

def load_onet_data():
    """
    Load O*NET data
    
    This would normally come from O*NET API or downloaded dataset
    For this implementation, we'll create a sample dataset
    """
    global ONET_OCCUPATIONS, ONET_SKILLS, ONET_ABILITIES, ONET_KNOWLEDGE
    
    # Create sample O*NET occupations
    ONET_OCCUPATIONS = create_sample_occupations()
    
    # Create sample skills, abilities, and knowledge
    for occupation in ONET_OCCUPATIONS:
        occ_code = occupation["code"]
        ONET_SKILLS[occ_code] = occupation.get("skills", [])
        ONET_ABILITIES[occ_code] = occupation.get("abilities", [])
        ONET_KNOWLEDGE[occ_code] = occupation.get("knowledge", [])
    
    return True

def get_onet_occupations():
    """
    Get all O*NET occupations
    
    Returns:
        list: List of occupation dictionaries
    """
    if not ONET_OCCUPATIONS:
        load_onet_data()
    return ONET_OCCUPATIONS

def get_occupation_details(occupation_code):
    """
    Get detailed information for a specific occupation
    
    Args:
        occupation_code: O*NET occupation code
        
    Returns:
        dict: Detailed occupation information
    """
    # Find occupation in the data
    occupation = None
    for occ in ONET_OCCUPATIONS:
        if occ["code"] == occupation_code:
            occupation = occ
            break
    
    if not occupation:
        return {"error": f"Occupation with code {occupation_code} not found"}
    
    # Gather detailed information
    details = {
        "code": occupation["code"],
        "title": occupation["title"],
        "description": occupation.get("description", ""),
        "skills": ONET_SKILLS.get(occupation_code, []),
        "abilities": ONET_ABILITIES.get(occupation_code, []),
        "knowledge": ONET_KNOWLEDGE.get(occupation_code, []),
        "salary_range": occupation.get("salary_range", {"min": 0, "max": 0, "median": 0}),
        "growth_outlook": occupation.get("growth_outlook", "Average"),
        "education_required": occupation.get("education_required", "Not specified"),
        "riasec_codes": occupation.get("riasec_codes", {})
    }
    
    return details

def create_sample_occupations():
    """
    Create sample O*NET occupation data for demonstration
    
    In a real application, this would come from the O*NET database
    
    Returns:
        list: Sample occupation data
    """
    return [
        {
            "code": "15-1252.00",
            "title": "Software Developer",
            "description": "Develop, create, and modify general computer applications software or specialized utility programs. Analyze user needs and develop software solutions. Design software or customize software for client use with the aim of optimizing operational efficiency. May analyze and design databases within an application area, working individually or coordinating database development as part of a team. May supervise computer programmers.",
            "skills": ["programming", "software development", "python", "java", "javascript", "c++", "sql", "database design", "web development", "algorithms", "data structures", "git", "problem solving", "critical thinking", "debugging"],
            "abilities": ["logical reasoning", "mathematical reasoning", "inductive reasoning", "deductive reasoning", "information ordering", "oral comprehension", "written comprehension", "oral expression", "written expression"],
            "knowledge": ["computers and electronics", "software development lifecycle", "agile methodology", "scrum", "mathematics", "engineering and technology", "english language", "telecommunications", "customer service"],
            "salary_range": {"min": 80000, "max": 150000, "median": 110000},
            "growth_outlook": "Much faster than average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 50, "investigative": 90, "artistic": 40, "social": 30, "enterprising": 20, "conventional": 70}
        },
        {
            "code": "15-2051.01",
            "title": "Data Scientist",
            "description": "Research, design, and develop computer and network software or specialized utility programs. Analyze user needs and develop software solutions, applying principles and techniques of computer science, engineering, and mathematical analysis. Update software or enhance existing software capabilities. May work with computer hardware engineers to integrate hardware and software systems, and develop specifications and performance requirements.",
            "skills": ["python", "r", "sql", "machine learning", "statistics", "data analysis", "data visualization", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "deep learning", "natural language processing", "big data"],
            "abilities": ["mathematical reasoning", "inductive reasoning", "deductive reasoning", "information ordering", "category flexibility", "pattern recognition", "statistical analysis", "problem solving", "critical thinking"],
            "knowledge": ["mathematics", "computers and electronics", "statistics", "artificial intelligence", "database management", "algorithms", "engineering and technology", "english language", "education and training"],
            "salary_range": {"min": 90000, "max": 165000, "median": 120000},
            "growth_outlook": "Much faster than average",
            "education_required": "Master's degree",
            "riasec_codes": {"realistic": 40, "investigative": 95, "artistic": 30, "social": 20, "enterprising": 30, "conventional": 60}
        },
        {
            "code": "11-3021.00",
            "title": "Computer and Information Systems Manager",
            "description": "Plan, direct, or coordinate activities in such fields as electronic data processing, information systems, systems analysis, and computer programming. May direct and coordinate the design, installation, and support of an organization's computer systems, including system upgrades. Provide future forecasting and strategic information technology planning.",
            "skills": ["leadership", "management", "project management", "strategic planning", "budgeting", "communication", "problem solving", "decision making", "team management", "it infrastructure", "systems analysis", "risk management", "negotiation", "conflict resolution", "presentation"],
            "abilities": ["oral comprehension", "oral expression", "written comprehension", "written expression", "problem sensitivity", "deductive reasoning", "inductive reasoning", "information ordering", "speech clarity", "speech recognition"],
            "knowledge": ["administration and management", "computers and electronics", "personnel and human resources", "english language", "customer service", "economics and accounting", "sales and marketing", "telecommunications", "law and government", "education and training"],
            "salary_range": {"min": 110000, "max": 200000, "median": 150000},
            "growth_outlook": "Faster than average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 30, "investigative": 60, "artistic": 20, "social": 50, "enterprising": 90, "conventional": 70}
        },
        {
            "code": "13-1161.00",
            "title": "Market Research Analyst",
            "description": "Research market conditions in local, regional, or national areas, or gather information to determine potential sales of a product or service, or create a marketing campaign. May gather information on competitors, prices, sales, and methods of marketing and distribution. May collect and analyze data using statistical software.",
            "skills": ["data analysis", "market research", "statistics", "spreadsheets", "survey design", "report writing", "presentation", "communication", "critical thinking", "problem solving", "sql", "python", "r", "data visualization", "research"],
            "abilities": ["written comprehension", "written expression", "oral comprehension", "oral expression", "inductive reasoning", "deductive reasoning", "information ordering", "category flexibility", "mathematical reasoning", "pattern recognition"],
            "knowledge": ["sales and marketing", "customer service", "english language", "computers and electronics", "mathematics", "economics and accounting", "administration and management", "education and training", "psychology", "communications and media"],
            "salary_range": {"min": 65000, "max": 130000, "median": 85000},
            "growth_outlook": "Faster than average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 20, "investigative": 80, "artistic": 30, "social": 40, "enterprising": 70, "conventional": 60}
        },
        {
            "code": "13-2011.00",
            "title": "Accountant",
            "description": "Examine, analyze, and interpret accounting records to prepare financial statements, give advice, or audit and evaluate statements prepared by others. Install or advise on systems of recording costs or other financial and budgetary data. May work in areas such as taxation, forensic accounting, public accounting, cost accounting, or management accounting.",
            "skills": ["accounting", "financial analysis", "tax preparation", "auditing", "financial reporting", "bookkeeping", "spreadsheets", "quickbooks", "sap", "communication", "attention to detail", "problem solving", "critical thinking", "time management", "organization"],
            "abilities": ["mathematical reasoning", "number facility", "deductive reasoning", "inductive reasoning", "information ordering", "category flexibility", "written comprehension", "written expression", "oral comprehension", "oral expression"],
            "knowledge": ["economics and accounting", "mathematics", "english language", "computers and electronics", "administration and management", "law and government", "customer service", "personnel and human resources", "education and training", "clerical"],
            "salary_range": {"min": 60000, "max": 120000, "median": 80000},
            "growth_outlook": "Average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 30, "investigative": 70, "artistic": 10, "social": 30, "enterprising": 50, "conventional": 90}
        },
        {
            "code": "11-2021.00",
            "title": "Marketing Manager",
            "description": "Plan, direct, or coordinate marketing policies and programs, such as determining the demand for products and services offered by a firm and its competitors, and identify potential customers. Develop pricing strategies with the goal of maximizing the firm's profits or share of the market while ensuring the firm's customers are satisfied. Oversee product development or monitor trends that indicate the need for new products and services.",
            "skills": ["marketing strategy", "digital marketing", "social media marketing", "brand management", "content marketing", "seo", "sem", "advertising", "market research", "leadership", "project management", "communication", "presentation", "creativity", "analytics"],
            "abilities": ["oral expression", "oral comprehension", "written expression", "written comprehension", "speech clarity", "originality", "fluency of ideas", "deductive reasoning", "inductive reasoning", "problem sensitivity"],
            "knowledge": ["sales and marketing", "communications and media", "customer service", "english language", "administration and management", "personnel and human resources", "psychology", "sociology and anthropology", "education and training", "computers and electronics"],
            "salary_range": {"min": 90000, "max": 170000, "median": 120000},
            "growth_outlook": "Faster than average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 10, "investigative": 50, "artistic": 70, "social": 60, "enterprising": 90, "conventional": 40}
        },
        {
            "code": "29-1141.00",
            "title": "Registered Nurse",
            "description": "Assess patient health problems and needs, develop and implement nursing care plans, and maintain medical records. Administer nursing care to ill, injured, convalescent, or disabled patients. May advise patients on health maintenance and disease prevention or provide case management. Licensing or registration required.",
            "skills": ["patient care", "medical terminology", "vital signs", "electronic medical records", "medication administration", "critical thinking", "communication", "compassion", "time management", "organization", "assessment", "patient education", "teamwork", "basic life support", "clinical experience"],
            "abilities": ["problem sensitivity", "inductive reasoning", "deductive reasoning", "oral comprehension", "oral expression", "written comprehension", "written expression", "speech clarity", "speech recognition", "information ordering"],
            "knowledge": ["medicine and dentistry", "psychology", "customer service", "therapy and counseling", "english language", "biology", "chemistry", "education and training", "personnel and human resources", "mathematics"],
            "salary_range": {"min": 60000, "max": 110000, "median": 75000},
            "growth_outlook": "Faster than average",
            "education_required": "Associate's degree",
            "riasec_codes": {"realistic": 60, "investigative": 70, "artistic": 20, "social": 90, "enterprising": 40, "conventional": 50}
        },
        {
            "code": "25-2021.00",
            "title": "Elementary School Teacher",
            "description": "Teach students basic academic, social, and other formative skills in public or private schools at the elementary level. May work with special education students. Prepare students for later grades by encouraging them to explore learning opportunities and to persevere with challenging tasks.",
            "skills": ["teaching", "classroom management", "curriculum development", "communication", "organization", "patience", "creativity", "lesson planning", "assessment", "interpersonal skills", "adaptability", "time management", "problem solving", "technology integration", "teamwork"],
            "abilities": ["oral expression", "oral comprehension", "written expression", "written comprehension", "speech clarity", "speech recognition", "originality", "fluency of ideas", "problem sensitivity", "inductive reasoning"],
            "knowledge": ["education and training", "english language", "psychology", "mathematics", "sociology and anthropology", "therapy and counseling", "communications and media", "history and archeology", "geography", "fine arts"],
            "salary_range": {"min": 45000, "max": 90000, "median": 60000},
            "growth_outlook": "Average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 20, "investigative": 50, "artistic": 60, "social": 95, "enterprising": 40, "conventional": 50}
        },
        {
            "code": "17-2051.00",
            "title": "Civil Engineer",
            "description": "Perform engineering duties in planning, designing, and overseeing construction and maintenance of building structures and facilities, such as roads, railroads, airports, bridges, harbors, channels, dams, irrigation projects, pipelines, power plants, and water and sewage systems. Includes civil engineers specializing in transportation engineering.",
            "skills": ["autocad", "civil 3d", "structural analysis", "project management", "engineering design", "technical writing", "mathematics", "problem solving", "critical thinking", "communication", "attention to detail", "teamwork", "organizational skills", "leadership", "computer-aided design"],
            "abilities": ["inductive reasoning", "deductive reasoning", "mathematical reasoning", "spatial orientation", "visualization", "information ordering", "problem sensitivity", "written comprehension", "written expression", "oral comprehension"],
            "knowledge": ["engineering and technology", "design", "building and construction", "mathematics", "physics", "english language", "computers and electronics", "administration and management", "education and training", "personnel and human resources"],
            "salary_range": {"min": 70000, "max": 130000, "median": 95000},
            "growth_outlook": "Average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 70, "investigative": 80, "artistic": 30, "social": 30, "enterprising": 50, "conventional": 60}
        },
        {
            "code": "13-2051.00",
            "title": "Financial Analyst",
            "description": "Conduct quantitative analyses of information affecting investment programs of public or private institutions. Perform financial forecasting, reporting, and operational metrics tracking, analyze financial data, create financial models, and make recommendations to senior management.",
            "skills": ["financial analysis", "excel", "financial modeling", "valuation", "forecasting", "data analysis", "accounting", "financial reporting", "statistical analysis", "problem solving", "critical thinking", "communication", "presentation", "attention to detail", "research"],
            "abilities": ["mathematical reasoning", "number facility", "deductive reasoning", "inductive reasoning", "information ordering", "category flexibility", "written comprehension", "written expression", "oral comprehension", "oral expression"],
            "knowledge": ["economics and accounting", "mathematics", "english language", "computers and electronics", "administration and management", "law and government", "sales and marketing", "customer service", "personnel and human resources", "education and training"],
            "salary_range": {"min": 70000, "max": 140000, "median": 95000},
            "growth_outlook": "Faster than average",
            "education_required": "Bachelor's degree",
            "riasec_codes": {"realistic": 20, "investigative": 80, "artistic": 10, "social": 30, "enterprising": 60, "conventional": 80}
        }
    ]
