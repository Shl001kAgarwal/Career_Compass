import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

from data.career_skill_dataset import get_career_skill_dataset
from data.onet_data import get_onet_occupations, get_occupation_details
from data.company_hiring_data import get_top_companies

class MLCareerRecommender:
    """Machine Learning based Career Recommendation Engine"""
    
    def __init__(self):
        """Initialize the ML-based career recommendation engine"""
        self.pipeline = None
        self.vectorizer = None
        self.job_titles = np.array([])
        self.feature_names = []
        self.classifier = None
        self.trained = False
    
    def train_model(self):
        """Train the ML model on career skill dataset"""
        # Get the dataset
        dataset = get_career_skill_dataset()
        
        if not dataset:
            st.error("Failed to load career skill dataset")
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(dataset)
        
        # Process the dataset
        X = df.copy()
        
        # Process skills - join them as text
        X['skills_text'] = X['skills'].apply(lambda x: ' '.join(x))
        
        # Get unique job titles
        self.job_titles = X['job_title'].unique()
        
        # Create one-hot encoded target for job titles
        y = pd.get_dummies(X['job_title'])
        
        # Create feature processing pipeline
        # 1. TF-IDF vectorization for skills text
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        try:
            skills_text_matrix = self.vectorizer.fit_transform(X['skills_text'])
            skills_text = skills_text_matrix.toarray()
        except Exception as e:
            st.error(f"Error in vectorization: {str(e)}")
            return False
        
        # Store feature names for later use
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Prepare features and target
        X_train = skills_text
        y_train = y.values
        
        # Train an XGBoost classifier for multi-output classification
        self.classifier = MultiOutputClassifier(
            XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=4,
                objective='binary:logistic'
            )
        )
        
        # Fit the model
        self.classifier.fit(X_train, y_train)
        
        self.trained = True
        return True
    
    def recommend_careers(self, user_profile, num_recommendations=5):
        """
        Generate career recommendations using ML model
        
        Args:
            user_profile: User's profile data
            num_recommendations: Number of recommendations to return
            
        Returns:
            list: Ranked list of career recommendations with details
        """
        # Check if model is trained
        if not self.trained:
            self.train_model()
            if not self.trained:
                st.error("Failed to train ML model")
                return []
        
        # Extract user skills
        user_skills = user_profile["technical_skills"] + user_profile["soft_skills"]
        user_skills_text = " ".join(user_skills)
        
        # Transform user skills using the vectorizer
        if self.vectorizer is None:
            st.error("Vectorizer not initialized")
            return []
            
        try:
            user_features_matrix = self.vectorizer.transform([user_skills_text])
            user_features = user_features_matrix.toarray()
        except Exception as e:
            st.error(f"Error transforming user skills: {str(e)}")
            return []
        
        # Predict probabilities for each job title
        if self.classifier is None:
            st.error("Classifier not initialized")
            return []
            
        try:
            job_probabilities = self.classifier.predict_proba(user_features)
        except Exception as e:
            st.error(f"Error predicting probabilities: {str(e)}")
            return []
        
        # Process the probabilities and get top job titles
        job_scores = {}
        
        # Make sure job_titles is not empty
        if len(self.job_titles) == 0:
            st.error("No job titles available for recommendation")
            return []
            
        for i, job_title in enumerate(self.job_titles):
            try:
                # Get the positive class probability for this job title
                class_idx = i  # Use index directly instead of searching again
                
                # Handle different structures of job_probabilities based on classifier
                if isinstance(job_probabilities, list) and len(job_probabilities) > class_idx:
                    probs = job_probabilities[class_idx]
                    if hasattr(probs, 'shape') and probs.shape[0] > 0:
                        # Get probability of positive class (class 1)
                        prob = probs[0][1] if probs.shape[1] > 1 else probs[0][0]
                    else:
                        prob = 0.5  # Default probability
                else:
                    prob = 0.5  # Default probability
                    
                job_scores[job_title] = prob
            except Exception:
                # If there's any error, assign a default score
                job_scores[job_title] = 0.5
        
        # Apply RIASEC weighting if available
        if user_profile["personality"] and "riasec" in user_profile["personality"]:
            # Get O*NET occupations
            occupations = get_onet_occupations()
            
            # Get user's RIASEC scores
            riasec_scores = user_profile["personality"]["riasec"]
            
            # Adjust scores based on RIASEC match
            for job_title in job_scores.keys():
                # Find matching occupation from O*NET
                occ = next((o for o in occupations if o["title"].lower() == job_title.lower()), None)
                
                if occ and "riasec_codes" in occ:
                    riasec_match = 0
                    for code, user_score in riasec_scores.items():
                        occ_score = occ["riasec_codes"].get(code, 0)
                        riasec_match += (user_score * occ_score) / 100
                    
                    # Blend ML score with RIASEC match (70% ML, 30% RIASEC)
                    job_scores[job_title] = job_scores[job_title] * 0.7 + riasec_match * 0.3
        
        # Sort job titles by score and get top N
        top_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:num_recommendations]
        
        # Get O*NET occupations
        occupations = get_onet_occupations()
        
        # Convert to recommendation format
        recommendations = []
        for job_title, score in top_jobs:
            # Find matching occupation
            occupation = next((o for o in occupations if o["title"].lower() == job_title.lower()), None)
            
            if not occupation:
                # Skip if no matching occupation found
                continue
            
            # Get details for this occupation
            occupation_details = get_occupation_details(occupation["code"])
            
            # Get top companies for this job
            top_companies = get_top_companies(job_title)
            
            # Calculate skill match
            user_skill_set = set([skill.lower() for skill in user_skills])
            occupation_skill_set = set([skill.lower() for skill in occupation.get("skills", [])])
            matching_skills = user_skill_set.intersection(occupation_skill_set)
            missing_skills = occupation_skill_set.difference(user_skill_set)
            skill_match_percentage = len(matching_skills) / len(occupation_skill_set) * 100 if occupation_skill_set else 0
            
            # Create recommendation object
            recommendation = {
                "title": occupation["title"],
                "code": occupation["code"],
                "description": occupation_details.get("description", ""),
                "match_score": int(score * 100),  # Convert to 0-100 scale
                "salary_range": occupation_details.get("salary_range", {"min": 0, "max": 0, "median": 0}),
                "growth_outlook": occupation_details.get("growth_outlook", "Average"),
                "education_required": occupation_details.get("education_required", "Not specified"),
                "matching_skills": list(matching_skills),
                "missing_skills": list(missing_skills),
                "skill_match_percentage": skill_match_percentage,
                "top_companies": top_companies
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def get_feature_importance(self, job_title):
        """
        Get feature importance for a specific job title
        
        Args:
            job_title: The job title to get feature importance for
            
        Returns:
            dict: Feature importance scores
        """
        if not self.trained:
            self.train_model()
            if not self.trained:
                return {}
        
        # Get the index of the job title
        if job_title not in self.job_titles:
            return {}
        
        job_idx = np.where(self.job_titles == job_title)[0][0]
        
        # Check if classifier and estimators are available
        if self.classifier is None or not hasattr(self.classifier, 'estimators_'):
            return {}
            
        # Get the feature importance for this job title
        try:
            importances = self.classifier.estimators_[job_idx].feature_importances_
            
            # Map feature importance to feature names
            importance_dict = {}
            for i, importance in enumerate(importances):
                if i < len(self.feature_names):
                    importance_dict[self.feature_names[i]] = float(importance)
            
            # Sort by importance
            importance_dict = {k: v for k, v in sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)}
            
            return importance_dict
        except (IndexError, AttributeError):
            # Handle cases where the classifier structure is not as expected
            return {}

# Create a singleton instance
ml_recommender = MLCareerRecommender()