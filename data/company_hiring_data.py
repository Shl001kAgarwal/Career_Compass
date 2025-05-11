import pandas as pd
import numpy as np

# Global variable to store company hiring data
COMPANY_HIRING_DATA = {}

def load_company_hiring_data():
    """
    Load company hiring data
    
    In a real application, this would load data from an API or database
    For this implementation, we'll create sample data
    """
    global COMPANY_HIRING_DATA
    
    # Generate sample company hiring data
    COMPANY_HIRING_DATA = create_sample_company_data()
    
    return True

def get_top_companies(job_title, num_companies=5):
    """
    Get top companies hiring for a specific job title
    
    Args:
        job_title: The job title to find companies for
        num_companies: Number of top companies to return
        
    Returns:
        list: List of top companies for the job title
    """
    if not COMPANY_HIRING_DATA:
        load_company_hiring_data()
    
    # Find most similar job title if exact match not found
    if job_title not in COMPANY_HIRING_DATA:
        similar_titles = find_similar_job_titles(job_title, list(COMPANY_HIRING_DATA.keys()))
        if similar_titles:
            job_title = similar_titles[0]
        else:
            return []  # No matching job title found
    
    # Return top companies
    return COMPANY_HIRING_DATA.get(job_title, [])[:num_companies]

def find_similar_job_titles(job_title, available_titles, threshold=0.7):
    """
    Find similar job titles using word overlap
    
    Args:
        job_title: The job title to match
        available_titles: List of available job titles
        threshold: Similarity threshold (0-1)
        
    Returns:
        list: List of similar job titles
    """
    job_title_lower = job_title.lower()
    job_words = set(job_title_lower.split())
    
    similarities = []
    for title in available_titles:
        title_lower = title.lower()
        title_words = set(title_lower.split())
        
        # Calculate Jaccard similarity
        intersection = len(job_words.intersection(title_words))
        union = len(job_words.union(title_words))
        similarity = intersection / union if union > 0 else 0
        
        if similarity >= threshold:
            similarities.append((title, similarity))
    
    # Sort by similarity and return titles
    return [title for title, sim in sorted(similarities, key=lambda x: x[1], reverse=True)]

def create_sample_company_data():
    """
    Create sample company hiring data
    
    Returns:
        dict: Dictionary of job titles with top hiring companies
    """
    return {
        "Software Developer": [
            {"name": "Microsoft", "hiring_frequency": 95, "avg_salary": 130000, "location": "Redmond, WA"},
            {"name": "Google", "hiring_frequency": 92, "avg_salary": 145000, "location": "Mountain View, CA"},
            {"name": "Amazon", "hiring_frequency": 90, "avg_salary": 135000, "location": "Seattle, WA"},
            {"name": "Facebook", "hiring_frequency": 87, "avg_salary": 150000, "location": "Menlo Park, CA"},
            {"name": "IBM", "hiring_frequency": 83, "avg_salary": 115000, "location": "Armonk, NY"},
            {"name": "Oracle", "hiring_frequency": 80, "avg_salary": 125000, "location": "Redwood City, CA"},
            {"name": "Salesforce", "hiring_frequency": 78, "avg_salary": 130000, "location": "San Francisco, CA"},
            {"name": "Apple", "hiring_frequency": 75, "avg_salary": 140000, "location": "Cupertino, CA"}
        ],
        
        "Data Scientist": [
            {"name": "Amazon", "hiring_frequency": 94, "avg_salary": 140000, "location": "Seattle, WA"},
            {"name": "Google", "hiring_frequency": 92, "avg_salary": 155000, "location": "Mountain View, CA"},
            {"name": "Microsoft", "hiring_frequency": 88, "avg_salary": 135000, "location": "Redmond, WA"},
            {"name": "Facebook", "hiring_frequency": 85, "avg_salary": 160000, "location": "Menlo Park, CA"},
            {"name": "IBM", "hiring_frequency": 82, "avg_salary": 130000, "location": "Armonk, NY"},
            {"name": "Uber", "hiring_frequency": 80, "avg_salary": 145000, "location": "San Francisco, CA"},
            {"name": "Netflix", "hiring_frequency": 78, "avg_salary": 165000, "location": "Los Gatos, CA"},
            {"name": "Airbnb", "hiring_frequency": 75, "avg_salary": 150000, "location": "San Francisco, CA"}
        ],
        
        "Computer and Information Systems Manager": [
            {"name": "Deloitte", "hiring_frequency": 90, "avg_salary": 155000, "location": "New York, NY"},
            {"name": "IBM", "hiring_frequency": 88, "avg_salary": 150000, "location": "Armonk, NY"},
            {"name": "Accenture", "hiring_frequency": 85, "avg_salary": 160000, "location": "Dublin, Ireland"},
            {"name": "Microsoft", "hiring_frequency": 83, "avg_salary": 170000, "location": "Redmond, WA"},
            {"name": "Oracle", "hiring_frequency": 81, "avg_salary": 165000, "location": "Redwood City, CA"},
            {"name": "Cognizant", "hiring_frequency": 78, "avg_salary": 145000, "location": "Teaneck, NJ"},
            {"name": "Cisco", "hiring_frequency": 76, "avg_salary": 160000, "location": "San Jose, CA"},
            {"name": "SAP", "hiring_frequency": 74, "avg_salary": 155000, "location": "Walldorf, Germany"}
        ],
        
        "Market Research Analyst": [
            {"name": "Nielsen", "hiring_frequency": 92, "avg_salary": 90000, "location": "New York, NY"},
            {"name": "Ipsos", "hiring_frequency": 89, "avg_salary": 85000, "location": "Paris, France"},
            {"name": "Kantar", "hiring_frequency": 87, "avg_salary": 88000, "location": "London, UK"},
            {"name": "Procter & Gamble", "hiring_frequency": 84, "avg_salary": 95000, "location": "Cincinnati, OH"},
            {"name": "McKinsey & Company", "hiring_frequency": 82, "avg_salary": 105000, "location": "New York, NY"},
            {"name": "Unilever", "hiring_frequency": 80, "avg_salary": 92000, "location": "London, UK"},
            {"name": "Boston Consulting Group", "hiring_frequency": 78, "avg_salary": 100000, "location": "Boston, MA"},
            {"name": "Google", "hiring_frequency": 76, "avg_salary": 110000, "location": "Mountain View, CA"}
        ],
        
        "Accountant": [
            {"name": "Deloitte", "hiring_frequency": 93, "avg_salary": 85000, "location": "New York, NY"},
            {"name": "PwC", "hiring_frequency": 91, "avg_salary": 87000, "location": "London, UK"},
            {"name": "EY", "hiring_frequency": 90, "avg_salary": 86000, "location": "London, UK"},
            {"name": "KPMG", "hiring_frequency": 88, "avg_salary": 84000, "location": "Amstelveen, Netherlands"},
            {"name": "Grant Thornton", "hiring_frequency": 85, "avg_salary": 80000, "location": "Chicago, IL"},
            {"name": "BDO", "hiring_frequency": 83, "avg_salary": 79000, "location": "Brussels, Belgium"},
            {"name": "RSM", "hiring_frequency": 80, "avg_salary": 78000, "location": "Chicago, IL"},
            {"name": "Baker Tilly", "hiring_frequency": 78, "avg_salary": 76000, "location": "Chicago, IL"}
        ],
        
        "Marketing Manager": [
            {"name": "Procter & Gamble", "hiring_frequency": 94, "avg_salary": 125000, "location": "Cincinnati, OH"},
            {"name": "Unilever", "hiring_frequency": 92, "avg_salary": 120000, "location": "London, UK"},
            {"name": "Coca-Cola", "hiring_frequency": 90, "avg_salary": 130000, "location": "Atlanta, GA"},
            {"name": "PepsiCo", "hiring_frequency": 88, "avg_salary": 128000, "location": "Purchase, NY"},
            {"name": "L'Oréal", "hiring_frequency": 86, "avg_salary": 115000, "location": "Paris, France"},
            {"name": "Johnson & Johnson", "hiring_frequency": 84, "avg_salary": 132000, "location": "New Brunswick, NJ"},
            {"name": "Nike", "hiring_frequency": 82, "avg_salary": 135000, "location": "Beaverton, OR"},
            {"name": "Amazon", "hiring_frequency": 80, "avg_salary": 140000, "location": "Seattle, WA"}
        ],
        
        "Registered Nurse": [
            {"name": "HCA Healthcare", "hiring_frequency": 95, "avg_salary": 78000, "location": "Nashville, TN"},
            {"name": "CommonSpirit Health", "hiring_frequency": 93, "avg_salary": 80000, "location": "Chicago, IL"},
            {"name": "Ascension", "hiring_frequency": 91, "avg_salary": 79000, "location": "St. Louis, MO"},
            {"name": "Kaiser Permanente", "hiring_frequency": 90, "avg_salary": 95000, "location": "Oakland, CA"},
            {"name": "Providence", "hiring_frequency": 88, "avg_salary": 85000, "location": "Renton, WA"},
            {"name": "Tenet Healthcare", "hiring_frequency": 86, "avg_salary": 77000, "location": "Dallas, TX"},
            {"name": "Cleveland Clinic", "hiring_frequency": 84, "avg_salary": 82000, "location": "Cleveland, OH"},
            {"name": "Mayo Clinic", "hiring_frequency": 82, "avg_salary": 88000, "location": "Rochester, MN"}
        ],
        
        "Elementary School Teacher": [
            {"name": "New York City Department of Education", "hiring_frequency": 92, "avg_salary": 65000, "location": "New York, NY"},
            {"name": "Los Angeles Unified School District", "hiring_frequency": 90, "avg_salary": 70000, "location": "Los Angeles, CA"},
            {"name": "Chicago Public Schools", "hiring_frequency": 88, "avg_salary": 62000, "location": "Chicago, IL"},
            {"name": "Miami-Dade County Public Schools", "hiring_frequency": 85, "avg_salary": 56000, "location": "Miami, FL"},
            {"name": "Clark County School District", "hiring_frequency": 83, "avg_salary": 55000, "location": "Las Vegas, NV"},
            {"name": "Houston Independent School District", "hiring_frequency": 81, "avg_salary": 58000, "location": "Houston, TX"},
            {"name": "Broward County Public Schools", "hiring_frequency": 79, "avg_salary": 54000, "location": "Fort Lauderdale, FL"},
            {"name": "Hawaii Department of Education", "hiring_frequency": 77, "avg_salary": 60000, "location": "Honolulu, HI"}
        ],
        
        "Civil Engineer": [
            {"name": "AECOM", "hiring_frequency": 93, "avg_salary": 95000, "location": "Los Angeles, CA"},
            {"name": "Jacobs", "hiring_frequency": 91, "avg_salary": 93000, "location": "Dallas, TX"},
            {"name": "Fluor", "hiring_frequency": 89, "avg_salary": 92000, "location": "Irving, TX"},
            {"name": "Bechtel", "hiring_frequency": 87, "avg_salary": 98000, "location": "Reston, VA"},
            {"name": "Kiewit", "hiring_frequency": 85, "avg_salary": 90000, "location": "Omaha, NE"},
            {"name": "HDR", "hiring_frequency": 83, "avg_salary": 88000, "location": "Omaha, NE"},
            {"name": "WSP", "hiring_frequency": 81, "avg_salary": 87000, "location": "Montreal, Canada"},
            {"name": "Stantec", "hiring_frequency": 79, "avg_salary": 86000, "location": "Edmonton, Canada"}
        ]
    }