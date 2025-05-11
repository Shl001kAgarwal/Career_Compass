import numpy as np
import pandas as pd
from data.sample_career_paths import get_career_progression_data, get_role_transition_matrix
from data.onet_data import get_occupation_details

def predict_career_trajectory(current_role, user_profile, time_horizon=10):
    """
    Predict potential career trajectory for a user
    
    Args:
        current_role: The user's current or target role
        user_profile: User's profile data
        time_horizon: Number of years to forecast (default: 10)
        
    Returns:
        dict: Career trajectory prediction
    """
    # Get career progression data
    progression_data = get_career_progression_data()
    transition_matrix = get_role_transition_matrix()
    
    # Find similar roles if current_role is not found
    role_key = current_role
    if current_role not in progression_data:
        # Find closest match
        role_key = find_similar_role(current_role, progression_data.keys())
    
    # Get progression paths for this role
    if role_key in progression_data:
        paths = progression_data[role_key]
    else:
        # Fallback to a generic path if no match found
        paths = create_generic_path(current_role)
    
    # Adjust paths based on user profile
    adjusted_paths = adjust_paths_for_user(paths, user_profile)
    
    # Calculate probabilities for each path
    path_probabilities = calculate_path_probabilities(adjusted_paths, transition_matrix)
    
    # Structure the result
    trajectory = {
        "starting_role": current_role,
        "time_horizon": time_horizon,
        "paths": []
    }
    
    # Process each career path
    for i, path in enumerate(adjusted_paths):
        # Limit the path to the time horizon
        limited_path = path[:time_horizon+1] if len(path) > time_horizon else path
        
        # Pad path if it's shorter than time horizon
        while len(limited_path) <= time_horizon:
            if limited_path:
                limited_path.append(limited_path[-1])
            else:
                limited_path.append(current_role)
        
        # Get details for each role in the path
        path_details = []
        for role in limited_path:
            # Get occupation details
            occupation_code = get_occupation_code_for_role(role)
            details = get_occupation_details(occupation_code) if occupation_code else {}
            
            role_detail = {
                "title": role,
                "salary": details.get("salary_range", {}).get("median", 0),
                "skills_required": details.get("skills", [])[:5],  # Top 5 skills
                "education": details.get("education_required", "Not specified")
            }
            
            path_details.append(role_detail)
        
        # Add path to trajectory
        trajectory["paths"].append({
            "path_details": path_details,
            "probability": path_probabilities[i],
            "description": generate_path_description(limited_path)
        })
    
    # Sort paths by probability
    trajectory["paths"] = sorted(trajectory["paths"], key=lambda x: x["probability"], reverse=True)
    
    return trajectory

def find_similar_role(role, available_roles):
    """Find the closest matching role from available roles"""
    # Simple string matching (in a real system, this would use more sophisticated NLP)
    role_lower = role.lower()
    best_match = None
    best_score = 0
    
    for available_role in available_roles:
        avail_lower = available_role.lower()
        # Calculate simple word overlap
        role_words = set(role_lower.split())
        avail_words = set(avail_lower.split())
        overlap = len(role_words.intersection(avail_words))
        
        if overlap > best_score:
            best_score = overlap
            best_match = available_role
    
    return best_match if best_score > 0 else list(available_roles)[0]

def create_generic_path(current_role):
    """Create a generic career path when no specific data is available"""
    return [
        [current_role, 
         f"Senior {current_role}", 
         f"{current_role} Manager", 
         f"Director of {current_role.split()[-1] if ' ' in current_role else current_role}", 
         f"VP of {current_role.split()[-1] if ' ' in current_role else current_role}"]
    ]

def adjust_paths_for_user(paths, user_profile):
    """Adjust career paths based on user's profile"""
    adjusted_paths = paths.copy()
    
    # Adjust based on education (simplified)
    education_level = get_education_level(user_profile)
    
    if education_level == "high":
        # Accelerate paths for highly educated users
        adjusted_paths = [fast_track_path(path) for path in adjusted_paths]
    elif education_level == "low":
        # Add more intermediate steps for users with less education
        adjusted_paths = [add_intermediate_steps(path) for path in adjusted_paths]
    
    # Add entrepreneurial path if user has leadership skills
    if has_leadership_skills(user_profile):
        entrepreneurial_path = create_entrepreneurial_path(paths[0][0])
        adjusted_paths.append(entrepreneurial_path)
    
    return adjusted_paths

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

def has_leadership_skills(user_profile):
    """Check if user has leadership skills"""
    if not user_profile or "soft_skills" not in user_profile:
        return False
    
    leadership_keywords = ["leadership", "management", "lead", "supervise", "direct", "coordinate"]
    user_skills = [skill.lower() for skill in user_profile["soft_skills"]]
    
    return any(keyword in skill for keyword in leadership_keywords for skill in user_skills)

def fast_track_path(path):
    """Accelerate a career path by skipping some intermediate steps"""
    if len(path) <= 2:
        return path
    
    # Skip every other role after the first one
    return [path[0]] + [path[i] for i in range(2, len(path), 2)]

def add_intermediate_steps(path):
    """Add intermediate steps to a career path"""
    if len(path) <= 1:
        return path
    
    new_path = [path[0]]
    
    for i in range(1, len(path)):
        # Add an intermediate step between roles
        prev_role = path[i-1]
        curr_role = path[i]
        
        if "senior" not in prev_role.lower() and "senior" not in curr_role.lower():
            new_path.append(f"Senior {prev_role}")
        
        new_path.append(curr_role)
    
    return new_path

def create_entrepreneurial_path(starting_role):
    """Create an entrepreneurial path starting from the given role"""
    role_base = starting_role.split()[-1] if ' ' in starting_role else starting_role
    
    return [
        starting_role,
        f"Senior {starting_role}",
        f"Independent {role_base} Consultant",
        f"{role_base} Practice Lead",
        f"Founder, {role_base} Solutions"
    ]

def calculate_path_probabilities(paths, transition_matrix):
    """Calculate probability for each career path"""
    # In a real system, this would use the transition matrix more effectively
    # This is a simplified implementation
    
    # Base probability distribution
    base_probability = 1.0 / len(paths)
    
    # Slightly adjust probabilities based on path length
    # Shorter paths are slightly more likely (simplified assumption)
    path_lengths = [len(path) for path in paths]
    max_length = max(path_lengths)
    
    probabilities = []
    for length in path_lengths:
        # Adjust probability inversely with length (longer paths less likely)
        length_factor = 1.0 - ((length - min(path_lengths)) / max(1, (max_length - min(path_lengths)))) * 0.3
        probabilities.append(base_probability * length_factor)
    
    # Normalize probabilities to sum to 1
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    
    return probabilities

def get_occupation_code_for_role(role):
    """Get the O*NET occupation code for a given role"""
    # This is a simplified implementation
    # In a real system, this would use a more sophisticated mapping
    
    # Convert role to lowercase for matching
    role_lower = role.lower()
    
    # Map some common roles to O*NET codes (simplified)
    role_mapping = {
        "software developer": "15-1252.00",
        "senior software developer": "15-1252.00",
        "software engineer": "15-1252.00",
        "senior software engineer": "15-1252.00",
        "lead software engineer": "15-1252.00",
        "software architect": "15-1252.00",
        "software development manager": "11-3021.00",
        "it manager": "11-3021.00",
        "director of engineering": "11-3021.00",
        "cto": "11-1021.00",
        "data analyst": "15-2051.00",
        "data scientist": "15-2051.01",
        "senior data scientist": "15-2051.01",
        "data science manager": "11-9121.00",
        "machine learning engineer": "15-2051.01",
        "ai researcher": "15-2051.01",
        "marketing specialist": "13-1161.00",
        "marketing manager": "11-2021.00",
        "digital marketing manager": "11-2021.00",
        "marketing director": "11-2021.00",
        "cmo": "11-1021.00",
        "accountant": "13-2011.00",
        "senior accountant": "13-2011.00",
        "accounting manager": "11-3031.00",
        "financial analyst": "13-2051.00",
        "finance manager": "11-3031.00",
        "cfo": "11-1021.00"
    }
    
    # Try to find an exact match
    if role_lower in role_mapping:
        return role_mapping[role_lower]
    
    # Try to find a partial match
    for key, code in role_mapping.items():
        if key in role_lower or role_lower in key:
            return code
    
    # Default to a generic code if no match found
    return "13-1071.00"  # Human Resources Specialist

def generate_path_description(path):
    """Generate a description for a career path"""
    if not path:
        return "No clear career path identified."
    
    if len(path) == 1:
        return f"Remain in current role as {path[0]}."
    
    start_role = path[0]
    end_role = path[-1]
    
    # Count the steps
    steps = len(path) - 1
    
    # Generate description
    if steps == 1:
        return f"Direct progression from {start_role} to {end_role}."
    elif steps == 2:
        middle = path[1]
        return f"Short progression from {start_role} through {middle} to {end_role}."
    else:
        key_steps = path[1:-1]
        step_text = ", ".join(key_steps)
        return f"Career path from {start_role} through {step_text}, to eventually reach {end_role}."
