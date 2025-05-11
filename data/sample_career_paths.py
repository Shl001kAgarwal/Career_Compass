import pandas as pd
import numpy as np

# Global variables to store career path data
CAREER_PROGRESSIONS = {}
ROLE_TRANSITIONS = {}

def load_career_paths():
    """
    Load career path data
    
    In a real application, this would load data from a database or API
    For this implementation, we'll create sample data
    """
    global CAREER_PROGRESSIONS, ROLE_TRANSITIONS
    
    # Generate sample career progression data
    CAREER_PROGRESSIONS = create_sample_career_progressions()
    
    # Generate sample role transition matrix
    ROLE_TRANSITIONS = create_sample_transition_matrix()
    
    return True

def get_career_progression_data():
    """
    Get career progression data
    
    Returns:
        dict: Career progression data
    """
    if not CAREER_PROGRESSIONS:
        load_career_paths()
    return CAREER_PROGRESSIONS

def get_role_transition_matrix():
    """
    Get role transition matrix
    
    Returns:
        dict: Role transition probabilities
    """
    if not ROLE_TRANSITIONS:
        load_career_paths()
    return ROLE_TRANSITIONS

def create_sample_career_progressions():
    """
    Create sample career progression paths
    
    Returns:
        dict: Dictionary where keys are starting roles and values are lists of possible career paths
    """
    progressions = {
        "Software Developer": [
            ["Software Developer", "Senior Software Developer", "Software Architect", "Lead Software Engineer", "Engineering Manager", "Director of Engineering", "CTO"],
            ["Software Developer", "Senior Software Developer", "DevOps Engineer", "DevOps Manager", "VP of Infrastructure"],
            ["Software Developer", "Senior Software Developer", "Product Manager", "Senior Product Manager", "Director of Product", "CPO"],
            ["Software Developer", "Data Scientist", "Senior Data Scientist", "Data Science Manager", "Director of AI/ML", "CTO"]
        ],
        
        "Data Analyst": [
            ["Data Analyst", "Senior Data Analyst", "Data Scientist", "Senior Data Scientist", "Data Science Manager", "Director of Analytics", "Chief Data Officer"],
            ["Data Analyst", "Business Analyst", "Senior Business Analyst", "Product Manager", "Senior Product Manager", "Director of Product"],
            ["Data Analyst", "Marketing Analyst", "Marketing Manager", "Director of Marketing", "CMO"]
        ],
        
        "Marketing Specialist": [
            ["Marketing Specialist", "Senior Marketing Specialist", "Marketing Manager", "Senior Marketing Manager", "Director of Marketing", "VP of Marketing", "CMO"],
            ["Marketing Specialist", "Digital Marketing Specialist", "Social Media Manager", "Brand Manager", "Director of Brand Strategy", "CMO"],
            ["Marketing Specialist", "Content Marketer", "Content Marketing Manager", "Content Strategy Director", "VP of Content", "CMO"]
        ],
        
        "Accountant": [
            ["Accountant", "Senior Accountant", "Accounting Manager", "Controller", "Finance Director", "CFO"],
            ["Accountant", "Financial Analyst", "Senior Financial Analyst", "Finance Manager", "Finance Director", "CFO"],
            ["Accountant", "Tax Accountant", "Tax Manager", "Tax Director", "Partner"]
        ],
        
        "Registered Nurse": [
            ["Registered Nurse", "Charge Nurse", "Nurse Manager", "Nursing Director", "Chief Nursing Officer"],
            ["Registered Nurse", "Nurse Practitioner", "Advanced Practice Nurse", "Clinical Director"],
            ["Registered Nurse", "Nursing Educator", "Clinical Instructor", "Professor of Nursing"]
        ],
        
        "Elementary School Teacher": [
            ["Elementary School Teacher", "Lead Teacher", "Instructional Coach", "Assistant Principal", "Principal", "District Administrator"],
            ["Elementary School Teacher", "Educational Specialist", "Curriculum Developer", "Director of Curriculum"],
            ["Elementary School Teacher", "Master Teacher", "Teacher Mentor", "Professional Development Coordinator", "Instructional Supervisor"]
        ],
        
        "Civil Engineer": [
            ["Civil Engineer", "Senior Civil Engineer", "Project Engineer", "Project Manager", "Engineering Manager", "Director of Engineering", "VP of Engineering"],
            ["Civil Engineer", "Structural Engineer", "Senior Structural Engineer", "Engineering Consultant", "Partner"],
            ["Civil Engineer", "Construction Manager", "Senior Construction Manager", "Construction Director", "VP of Construction"]
        ],
        
        "Financial Analyst": [
            ["Financial Analyst", "Senior Financial Analyst", "Finance Manager", "Finance Director", "VP of Finance", "CFO"],
            ["Financial Analyst", "Investment Analyst", "Portfolio Manager", "Investment Director", "Chief Investment Officer"],
            ["Financial Analyst", "Risk Analyst", "Risk Manager", "Director of Risk Management", "Chief Risk Officer"]
        ]
    }
    
    return progressions

def create_sample_transition_matrix():
    """
    Create a sample role transition matrix
    
    In a real system, this would be calculated from real career progression data
    
    Returns:
        dict: Transition probabilities between roles
    """
    # This is a highly simplified transition matrix
    # In a real system, this would be much more comprehensive
    
    transitions = {
        "Software Developer": {
            "Senior Software Developer": 0.7,
            "Data Scientist": 0.15,
            "DevOps Engineer": 0.1,
            "Product Manager": 0.05
        },
        "Senior Software Developer": {
            "Software Architect": 0.4,
            "Lead Software Engineer": 0.3,
            "DevOps Engineer": 0.1,
            "Product Manager": 0.1,
            "Engineering Manager": 0.1
        },
        "Data Analyst": {
            "Senior Data Analyst": 0.6,
            "Business Analyst": 0.2,
            "Marketing Analyst": 0.1,
            "Data Scientist": 0.1
        },
        "Marketing Specialist": {
            "Senior Marketing Specialist": 0.5,
            "Digital Marketing Specialist": 0.3,
            "Content Marketer": 0.2
        },
        "Accountant": {
            "Senior Accountant": 0.6,
            "Financial Analyst": 0.2,
            "Tax Accountant": 0.2
        }
    }
    
    return transitions
