import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from data.onet_data import get_onet_occupations, get_occupation_details
from data.company_hiring_data import get_top_companies
from utils.ml_recommendation_engine import ml_recommender

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
    Generate career recommendations based on user profile using ML
    
    Args:
        user_profile: User's profile data
        num_recommendations: Number of recommendations to return
        
    Returns:
        list: Ranked list of career recommendations with details
    """
    # Use the ML-based recommender
    recommendations = ml_recommender.recommend_careers(user_profile, num_recommendations)
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
    
    # Top hiring companies
    if 'top_companies' in recommendation and recommendation['top_companies']:
        explanation += f"\n* **Top companies hiring {recommendation['title']}s:**\n"
        for company in recommendation['top_companies'][:3]:
            explanation += f"  - {company['name']} (Avg. salary: ${company['avg_salary']:,})\n"
    
    return explanation
