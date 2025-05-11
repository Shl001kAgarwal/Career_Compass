import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data.course_data import get_available_courses

def recommend_courses(missing_skills, user_profile=None, num_recommendations=5):
    """
    Recommend courses based on missing skills
    
    Args:
        missing_skills: List of skills the user is missing
        user_profile: User's profile data (optional)
        num_recommendations: Number of courses to recommend per skill
        
    Returns:
        dict: Dictionary of recommended courses by skill
    """
    # Get available courses
    all_courses = get_available_courses()
    
    # Convert missing skills to string for TF-IDF
    skill_texts = [" ".join(skill.split("_")) for skill in missing_skills]
    
    # Create course description texts
    course_texts = [f"{course['title']} {course['description']}" for course in all_courses]
    
    # Calculate relevance using TF-IDF and cosine similarity
    vectorizer = TfidfVectorizer()
    course_vectors = vectorizer.fit_transform(course_texts)
    
    recommendations = {}
    
    for skill in missing_skills:
        # Clean skill text
        skill_text = " ".join(skill.split("_"))
        
        # Transform skill to vector
        skill_vector = vectorizer.transform([skill_text])
        
        # Calculate similarity
        similarity_scores = cosine_similarity(skill_vector, course_vectors).flatten()
        
        # Apply personalization if user profile is available
        if user_profile:
            similarity_scores = personalize_recommendations(similarity_scores, all_courses, user_profile)
        
        # Get top courses
        top_indices = similarity_scores.argsort()[-num_recommendations:][::-1]
        skill_recommendations = [all_courses[i] for i in top_indices]
        
        # Add to recommendations
        recommendations[skill] = skill_recommendations
    
    return recommendations

def personalize_recommendations(similarity_scores, courses, user_profile):
    """
    Personalize course recommendations based on user profile
    
    Args:
        similarity_scores: Base similarity scores
        courses: List of available courses
        user_profile: User's profile data
        
    Returns:
        numpy.array: Adjusted similarity scores
    """
    # Copy scores to avoid modifying original
    adjusted_scores = similarity_scores.copy()
    
    # Adjust based on education level
    education_level = get_education_level(user_profile)
    for i, course in enumerate(courses):
        course_level = course.get("difficulty", "intermediate")
        
        # Match course level with user education
        if education_level == "high" and course_level == "advanced":
            adjusted_scores[i] *= 1.2  # Boost advanced courses for highly educated users
        elif education_level == "low" and course_level == "beginner":
            adjusted_scores[i] *= 1.2  # Boost beginner courses for users with less education
    
    # Adjust based on learning preferences if available
    if "personality" in user_profile and "learning_style" in user_profile["personality"]:
        learning_style = user_profile["personality"]["learning_style"]
        
        for i, course in enumerate(courses):
            course_format = course.get("format", "")
            
            # Match course format with learning style (simplified)
            if learning_style == "visual" and "video" in course_format.lower():
                adjusted_scores[i] *= 1.1
            elif learning_style == "reading" and "text" in course_format.lower():
                adjusted_scores[i] *= 1.1
            elif learning_style == "practical" and "project" in course_format.lower():
                adjusted_scores[i] *= 1.1
    
    return adjusted_scores

def get_education_level(user_profile):
    """Determine user's education level"""
    if not user_profile or "education" not in user_profile:
        return "medium"
    
    education = " ".join(user_profile["education"]).lower()
    
    if "phd" in education or "doctorate" in education or "master" in education:
        return "high"
    elif "bachelor" in education or "university" in education or "college" in education:
        return "medium"
    else:
        return "low"

def format_course_recommendations(course_recommendations):
    """
    Format course recommendations for display
    
    Args:
        course_recommendations: Dictionary of recommended courses by skill
        
    Returns:
        dict: Formatted recommendations
    """
    formatted = {}
    
    for skill, courses in course_recommendations.items():
        formatted_courses = []
        
        for course in courses:
            formatted_course = {
                "title": course["title"],
                "provider": course["provider"],
                "url": course["url"],
                "duration": course["duration"],
                "cost": course["cost"],
                "format": course["format"],
                "difficulty": course["difficulty"],
                "description_short": course["description"][:100] + "..." if len(course["description"]) > 100 else course["description"]
            }
            
            formatted_courses.append(formatted_course)
        
        formatted[skill] = formatted_courses
    
    return formatted
