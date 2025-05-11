import pandas as pd
import numpy as np

# Global variable to store course data
AVAILABLE_COURSES = []

def load_course_data():
    """
    Load course data
    
    In a real application, this would load data from an API like Coursera, Udemy, etc.
    For this implementation, we'll create sample data
    """
    global AVAILABLE_COURSES
    
    # Generate sample course data
    AVAILABLE_COURSES = create_sample_courses()
    
    return True

def get_available_courses():
    """
    Get all available courses
    
    Returns:
        list: List of available courses
    """
    if not AVAILABLE_COURSES:
        load_course_data()
    return AVAILABLE_COURSES

def create_sample_courses():
    """
    Create sample course data
    
    Returns:
        list: Sample course data
    """
    return [
        {
            "id": 1001,
            "title": "Python for Data Science and Machine Learning",
            "provider": "Udemy",
            "url": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/",
            "description": "Learn how to use NumPy, Pandas, Seaborn, Matplotlib, Plotly, Scikit-Learn, Machine Learning, TensorFlow, and more!",
            "skills": ["python", "data science", "machine learning", "numpy", "pandas", "matplotlib", "scikit-learn", "tensorflow"],
            "format": "Video, Projects",
            "duration": "40 hours",
            "difficulty": "intermediate",
            "cost": "$59.99"
        },
        {
            "id": 1002,
            "title": "Machine Learning A-Z: Hands-On Python & R",
            "provider": "Udemy",
            "url": "https://www.udemy.com/course/machinelearning/",
            "description": "Learn to create Machine Learning Algorithms in Python and R from two Data Science experts.",
            "skills": ["machine learning", "python", "r", "data science", "statistical analysis", "deep learning", "artificial intelligence"],
            "format": "Video, Projects",
            "duration": "44 hours",
            "difficulty": "intermediate",
            "cost": "$59.99"
        },
        {
            "id": 1003,
            "title": "Data Science Specialization",
            "provider": "Coursera (Johns Hopkins University)",
            "url": "https://www.coursera.org/specializations/jhu-data-science",
            "description": "Launch your career in data science. A ten-course introduction to data science, developed and taught by leading professors.",
            "skills": ["data science", "r programming", "statistical analysis", "data cleaning", "data visualization", "machine learning", "regression models", "reproducible research"],
            "format": "Video, Quizzes, Projects",
            "duration": "8 months",
            "difficulty": "intermediate",
            "cost": "$49/month"
        },
        {
            "id": 1004,
            "title": "Deep Learning Specialization",
            "provider": "Coursera (deeplearning.ai)",
            "url": "https://www.coursera.org/specializations/deep-learning",
            "description": "Become a Deep Learning Expert. Master Deep Learning and Break into AI.",
            "skills": ["deep learning", "neural networks", "convolutional neural networks", "tensorflow", "keras", "sequence models", "natural language processing", "computer vision"],
            "format": "Video, Programming Assignments",
            "duration": "3 months",
            "difficulty": "advanced",
            "cost": "$49/month"
        },
        {
            "id": 1005,
            "title": "JavaScript Algorithms and Data Structures",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
            "description": "Learn the fundamentals of JavaScript including variables, arrays, objects, loops, and functions. Create algorithms to manipulate strings, factorialize numbers, and more.",
            "skills": ["javascript", "algorithms", "data structures", "programming", "problem solving", "debugging"],
            "format": "Interactive, Projects",
            "duration": "300 hours",
            "difficulty": "beginner",
            "cost": "Free"
        },
        {
            "id": 1006,
            "title": "Full Stack Web Development with React",
            "provider": "Coursera (The Hong Kong University of Science and Technology)",
            "url": "https://www.coursera.org/specializations/full-stack-react",
            "description": "Build Complete Web and Hybrid Mobile Solutions. Master front-end web, hybrid mobile app and server-side development in three comprehensive courses.",
            "skills": ["react", "javascript", "node.js", "express.js", "mongodb", "front-end development", "back-end development", "full stack development", "responsive design"],
            "format": "Video, Projects",
            "duration": "3 months",
            "difficulty": "intermediate",
            "cost": "$49/month"
        },
        {
            "id": 1007,
            "title": "Google Project Management Certificate",
            "provider": "Coursera (Google)",
            "url": "https://www.coursera.org/professional-certificates/google-project-management",
            "description": "Start your path to a career in project management. In this program, you'll learn in-demand skills that will have you job-ready in less than six months.",
            "skills": ["project management", "agile project management", "scrum", "leadership", "communication", "risk management", "team management", "planning"],
            "format": "Video, Quizzes, Projects",
            "duration": "6 months",
            "difficulty": "beginner",
            "cost": "$39/month"
        },
        {
            "id": 1008,
            "title": "AWS Certified Solutions Architect - Associate",
            "provider": "A Cloud Guru",
            "url": "https://acloudguru.com/course/aws-certified-solutions-architect-associate",
            "description": "This course will help you master the core services of Amazon Web Services and prepare you for the AWS Certified Solutions Architect - Associate exam.",
            "skills": ["aws", "cloud computing", "s3", "ec2", "lambda", "iam", "vpc", "cloud architecture", "serverless"],
            "format": "Video, Hands-on Labs, Quizzes",
            "duration": "40 hours",
            "difficulty": "intermediate",
            "cost": "$149"
        },
        {
            "id": 1009,
            "title": "Financial Accounting Fundamentals",
            "provider": "Coursera (University of Virginia)",
            "url": "https://www.coursera.org/learn/uva-darden-financial-accounting",
            "description": "This course will teach you the fundamentals of financial accounting—how to read a balance sheet, income statement, and cash flow statement.",
            "skills": ["accounting", "financial accounting", "balance sheets", "income statements", "cash flow statements", "financial analysis", "financial reporting"],
            "format": "Video, Readings, Quizzes",
            "duration": "4 weeks",
            "difficulty": "beginner",
            "cost": "Free to audit"
        },
        {
            "id": 1010,
            "title": "Content Marketing Specialization",
            "provider": "Coursera (University of California, Davis)",
            "url": "https://www.coursera.org/specializations/content-marketing",
            "description": "Master Content Marketing Strategy, Content Creation, Content Distribution, and Content Measurement. Drive customer behavior online.",
            "skills": ["content marketing", "marketing strategy", "seo", "social media marketing", "content creation", "digital marketing", "brand management", "content measurement"],
            "format": "Video, Readings, Projects",
            "duration": "5 months",
            "difficulty": "intermediate",
            "cost": "$49/month"
        },
        {
            "id": 1011,
            "title": "Excel Skills for Business Specialization",
            "provider": "Coursera (Macquarie University)",
            "url": "https://www.coursera.org/specializations/excel",
            "description": "Master Excel for Business. Gain the Excel skills you need to succeed in the business world.",
            "skills": ["excel", "spreadsheets", "data analysis", "financial analysis", "pivot tables", "vlookup", "data visualization", "business analysis"],
            "format": "Video, Hands-on Exercises",
            "duration": "4 months",
            "difficulty": "beginner to intermediate",
            "cost": "$49/month"
        },
        {
            "id": 1012,
            "title": "Leadership and Management Specialization",
            "provider": "Coursera (Northwestern University)",
            "url": "https://www.coursera.org/specializations/leadership-management",
            "description": "Build Leadership Skills for Success in the Workplace. Develop critical skills needed for effective and efficient management as a supervisor, manager, or team leader.",
            "skills": ["leadership", "management", "organizational leadership", "communication", "coaching", "conflict management", "team management", "strategic leadership"],
            "format": "Video, Readings, Discussions, Projects",
            "duration": "6 months",
            "difficulty": "intermediate",
            "cost": "$49/month"
        },
        {
            "id": 1013,
            "title": "UX Design Fundamentals",
            "provider": "Interaction Design Foundation",
            "url": "https://www.interaction-design.org/courses/ux-design-fundamentals",
            "description": "This course will teach you the fundamentals of UX design and how to apply them to create products that provide meaningful and relevant experiences to users.",
            "skills": ["ux design", "user research", "information architecture", "wireframing", "prototyping", "usability testing", "interaction design", "user-centered design"],
            "format": "Video, Readings, Exercises, Projects",
            "duration": "10 weeks",
            "difficulty": "beginner",
            "cost": "$16/month (membership)"
        },
        {
            "id": 1014,
            "title": "CompTIA Security+ Certification",
            "provider": "Pluralsight",
            "url": "https://www.pluralsight.com/paths/comptia-security-sy0-601",
            "description": "This path is designed to help you prepare for the CompTIA Security+ exam, which certifies the essential skills required for network security and risk management.",
            "skills": ["cybersecurity", "network security", "security protocols", "risk management", "cryptography", "identity management", "access control", "threat detection"],
            "format": "Video, Quizzes, Hands-on Labs",
            "duration": "27 hours",
            "difficulty": "intermediate",
            "cost": "$29/month (subscription)"
        },
        {
            "id": 1015,
            "title": "Digital Marketing Specialization",
            "provider": "Coursera (University of Illinois)",
            "url": "https://www.coursera.org/specializations/digital-marketing",
            "description": "Master Strategic Marketing Concepts and Tools. Learn the fundamentals of marketing in a digital world and drive customer action online.",
            "skills": ["digital marketing", "seo", "social media marketing", "content marketing", "email marketing", "google analytics", "pay-per-click advertising", "marketing analytics"],
            "format": "Video, Readings, Projects",
            "duration": "8 months",
            "difficulty": "intermediate",
            "cost": "$49/month"
        }
    ]
