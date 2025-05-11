import streamlit as st
from data.onet_data import load_onet_data
from data.sample_career_paths import load_career_paths
from data.course_data import load_course_data
from data.company_hiring_data import load_company_hiring_data
from data.career_skill_dataset import load_career_skill_dataset

def load_initial_data():
    """
    Load initial data required for the application
    """
    # Use st.cache_data to ensure data is only loaded once
    load_onet_data_cached()
    load_career_paths_cached()
    load_course_data_cached()
    load_company_hiring_data_cached()
    load_career_skill_dataset_cached()

# Cache data loading functions to improve performance
@st.cache_data
def load_onet_data_cached():
    """Load O*NET data with caching"""
    return load_onet_data()

@st.cache_data
def load_career_paths_cached():
    """Load career path data with caching"""
    return load_career_paths()

@st.cache_data
def load_course_data_cached():
    """Load course data with caching"""
    return load_course_data()

@st.cache_data
def load_company_hiring_data_cached():
    """Load company hiring data with caching"""
    return load_company_hiring_data()

@st.cache_data
def load_career_skill_dataset_cached():
    """Load career skill dataset with caching"""
    return load_career_skill_dataset()
