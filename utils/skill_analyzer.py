import pandas as pd
import numpy as np
from data.onet_data import get_onet_occupations, get_occupation_details

def analyze_skill_gaps(user_skills, recommended_careers):
    """
    Analyze skill gaps between user's skills and recommended careers
    
    Args:
        user_skills: List of user's current skills
        recommended_careers: List of recommended career objects
        
    Returns:
        dict: Detailed skill gap analysis
    """
    user_skill_set = set([skill.lower() for skill in user_skills])
    
    skill_gaps = {}
    
    for career in recommended_careers:
        career_title = career["title"]
        occupation_details = get_occupation_details(career["code"])
        
        # Required skills for this occupation
        required_skills = set([skill.lower() for skill in occupation_details.get("skills", [])])
        required_abilities = set([ability.lower() for ability in occupation_details.get("abilities", [])])
        required_knowledge = set([knowledge.lower() for knowledge in occupation_details.get("knowledge", [])])
        
        all_required = required_skills.union(required_abilities).union(required_knowledge)
        
        # Identify missing skills
        missing_skills = all_required.difference(user_skill_set)
        
        # Calculate completion percentage
        total_required = len(all_required)
        skills_possessed = total_required - len(missing_skills)
        completion_percentage = (skills_possessed / total_required * 100) if total_required > 0 else 100
        
        # Categorize missing skills
        categorized_missing = {
            "technical": [skill for skill in missing_skills if skill in required_skills],
            "abilities": [skill for skill in missing_skills if skill in required_abilities],
            "knowledge": [skill for skill in missing_skills if skill in required_knowledge]
        }
        
        # Prioritize skills based on importance (simplified implementation)
        # In a real system, this would use O*NET importance ratings
        all_missing = list(missing_skills)
        prioritized_skills = sorted(all_missing, key=lambda x: len(x), reverse=True)[:10]
        
        skill_gaps[career_title] = {
            "completion_percentage": completion_percentage,
            "skills_possessed": skills_possessed,
            "total_required": total_required,
            "missing_skills": categorized_missing,
            "prioritized_skills": prioritized_skills
        }
    
    return skill_gaps

def recommend_skill_development_paths(skill_gaps, user_profile):
    """
    Recommend skill development paths based on skill gaps
    
    Args:
        skill_gaps: Dictionary of skill gaps by career
        user_profile: User's profile data
        
    Returns:
        dict: Skill development recommendations
    """
    development_paths = {}
    
    for career, gap_data in skill_gaps.items():
        # Extract priority skills to develop
        priority_skills = gap_data["prioritized_skills"]
        
        # Create development path
        path = {
            "skills_to_develop": priority_skills,
            "estimated_time": estimate_development_time(priority_skills, user_profile),
            "development_strategy": create_development_strategy(priority_skills)
        }
        
        development_paths[career] = path
    
    return development_paths

def estimate_development_time(skills, user_profile):
    """
    Estimate time needed to develop given skills
    
    Args:
        skills: List of skills to develop
        user_profile: User's profile data
        
    Returns:
        dict: Time estimates for skill development
    """
    # This is a simplified estimation model
    # In a real system, this would be based on more complex factors
    
    # Estimate time based on number of skills and user's background
    total_skills = len(skills)
    
    # Adjust based on education level (simplified)
    education_factor = 1.0
    if user_profile and "education" in user_profile:
        education = " ".join(user_profile["education"]).lower()
        if "phd" in education or "doctorate" in education:
            education_factor = 0.7
        elif "master" in education:
            education_factor = 0.8
        elif "bachelor" in education:
            education_factor = 0.9
    
    # Calculate time estimates (simplified model)
    # Assuming average 2 months per skill with adjustments
    months_per_skill = 2 * education_factor
    total_months = total_skills * months_per_skill
    
    # Create time breakdown
    if total_months < 3:
        time_frame = "Short-term (< 3 months)"
    elif total_months < 6:
        time_frame = "Medium-term (3-6 months)"
    elif total_months < 12:
        time_frame = "Long-term (6-12 months)"
    else:
        time_frame = "Extended (> 12 months)"
    
    return {
        "total_months": round(total_months, 1),
        "time_frame": time_frame,
        "intensity": "Part-time" if total_months > 6 else "Intensive"
    }

def create_development_strategy(skills):
    """
    Create a strategy for developing skills
    
    Args:
        skills: List of skills to develop
        
    Returns:
        list: Strategic recommendations for skill development
    """
    strategies = []
    
    # General recommendations
    if len(skills) > 5:
        strategies.append({
            "type": "sequencing",
            "description": "Focus on developing these skills in sequence rather than simultaneously"
        })
    
    # Add generic strategies (in a real system this would be more specific)
    strategies.append({
        "type": "formal_education",
        "description": "Consider courses or certifications for technical skills"
    })
    
    strategies.append({
        "type": "self_learning",
        "description": "Leverage online platforms like Coursera, Udemy, or LinkedIn Learning"
    })
    
    strategies.append({
        "type": "practical_application",
        "description": "Apply skills in projects to gain practical experience"
    })
    
    strategies.append({
        "type": "networking",
        "description": "Connect with professionals who possess these skills"
    })
    
    return strategies
