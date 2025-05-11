import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from data.onet_data import get_onet_occupations, get_occupation_details

def create_user_profile(resume_data, skills_data, personality_data):
    """
    Create a unified user profile from various data sources
    
    Args:
        resume_data: Parsed resume data
        skills_data: User-confirmed skills data
        personality_data: Personality assessment results
        
    Returns:
        dict: A unified user profile
    """
    # Extract and combine skills
    technical_skills = skills_data.get("technical", [])
    if resume_data and "skills" in resume_data:
        resume_tech_skills = resume_data["skills"].get("technical", [])
        technical_skills = list(set(technical_skills + resume_tech_skills))
    
    soft_skills = skills_data.get("soft", [])
    if resume_data and "skills" in resume_data:
        resume_soft_skills = resume_data["skills"].get("soft", [])
        soft_skills = list(set(soft_skills + resume_soft_skills))
    
    # Combine education info
    education = []
    if resume_data and "education" in resume_data:
        education = resume_data["education"]
    
    # Combine experience
    experience = []
    if resume_data and "experience" in resume_data:
        experience = resume_data["experience"]
    
    # Create the unified profile
    profile = {
        "technical_skills": technical_skills,
        "soft_skills": soft_skills,
        "education": education,
        "experience": experience,
        "personality": personality_data
    }
    
    return profile

def recommend_careers(user_profile, num_recommendations=5):
    """
    Generate career recommendations based on user profile
    
    Args:
        user_profile: User's profile data
        num_recommendations: Number of recommendations to return
        
    Returns:
        list: Ranked list of career recommendations with details
    """
    # Get O*NET occupations data
    occupations = get_onet_occupations()
    
    # Prepare skill-based matching
    user_skills = user_profile["technical_skills"] + user_profile["soft_skills"]
    user_skills_text = " ".join(user_skills).lower()
    
    # Create occupation skill texts
    occupation_skill_texts = []
    for occ in occupations:
        skills_text = " ".join(occ.get("skills", [])).lower()
        abilities_text = " ".join(occ.get("abilities", [])).lower()
        knowledge_text = " ".join(occ.get("knowledge", [])).lower()
        combined_text = f"{skills_text} {abilities_text} {knowledge_text}"
        occupation_skill_texts.append(combined_text)
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    occupation_vectors = vectorizer.fit_transform(occupation_skill_texts)
    user_vector = vectorizer.transform([user_skills_text])
    
    # Calculate similarity scores
    similarity_scores = cosine_similarity(user_vector, occupation_vectors).flatten()
    
    # Apply personality-based weighting if available
    if user_profile["personality"]:
        # Example: adjust scores based on Holland RIASEC codes
        riasec_scores = user_profile["personality"].get("riasec", {})
        for i, occ in enumerate(occupations):
            # Get occupation's RIASEC codes
            occ_riasec = occ.get("riasec_codes", {})
            
            # Calculate RIASEC match score (simplified)
            riasec_match = 0
            for code, user_score in riasec_scores.items():
                occ_score = occ_riasec.get(code, 0)
                riasec_match += (user_score * occ_score) / 100
            
            # Adjust similarity score with personality match
            similarity_scores[i] = similarity_scores[i] * 0.7 + riasec_match * 0.3
    
    # Get top recommendations
    top_indices = similarity_scores.argsort()[-num_recommendations:][::-1]
    
    # Create recommendation results with details
    recommendations = []
    for idx in top_indices:
        occupation = occupations[idx]
        
        # Get detailed information for this occupation
        occupation_details = get_occupation_details(occupation["code"])
        
        # Calculate match score (normalized to 0-100)
        match_score = int(similarity_scores[idx] * 100)
        
        # Calculate skill match
        user_skill_set = set(user_skills)
        occupation_skill_set = set(occupation.get("skills", []))
        matching_skills = user_skill_set.intersection(occupation_skill_set)
        skill_match_percentage = len(matching_skills) / len(occupation_skill_set) * 100 if occupation_skill_set else 0
        
        # Identify missing skills
        missing_skills = occupation_skill_set.difference(user_skill_set)
        
        recommendation = {
            "title": occupation["title"],
            "code": occupation["code"],
            "description": occupation_details.get("description", ""),
            "match_score": match_score,
            "salary_range": occupation_details.get("salary_range", {"min": 0, "max": 0, "median": 0}),
            "growth_outlook": occupation_details.get("growth_outlook", "Average"),
            "education_required": occupation_details.get("education_required", "Not specified"),
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "skill_match_percentage": skill_match_percentage
        }
        
        recommendations.append(recommendation)
    
    return recommendations

def explain_recommendation(recommendation):
    """
    Generate an explanation for why a career was recommended
    
    Args:
        recommendation: The career recommendation object
        
    Returns:
        str: Human-readable explanation
    """
    explanation = f"**{recommendation['title']}** was recommended because:\n\n"
    
    # Skill match explanation
    if recommendation['matching_skills']:
        explanation += f"* You possess {len(recommendation['matching_skills'])} relevant skills for this role "
        explanation += f"({int(recommendation['skill_match_percentage'])}% of required skills)\n"
        explanation += f"* Key matching skills: {', '.join(recommendation['matching_skills'][:5])}\n\n"
    
    # Missing skills explanation
    if recommendation['missing_skills']:
        explanation += f"* To be more competitive, consider developing these skills: "
        explanation += f"{', '.join(recommendation['missing_skills'][:5])}\n\n"
    
    # Education and outlook
    explanation += f"* This role typically requires: {recommendation['education_required']}\n"
    explanation += f"* Career outlook: {recommendation['growth_outlook']}\n"
    explanation += f"* Typical salary range: ${recommendation['salary_range']['min']:,} - ${recommendation['salary_range']['max']:,}\n"
    
    return explanation
