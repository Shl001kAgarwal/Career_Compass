# Career_Compass

A brief and friendly README template for the Career_Compass project. Replace placeholder sections with project-specific details (tech stack, commands, screenshots) to make this README fully accurate for your repository.

## Table of contents
- [About](#about)
- [Features](#features)
- [How it works](#working)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Command to run locally](#command_to_run_locally)
- [Contributing](#contributing)
- [Roadmap](#roadmap)

## About
Career Compass is an AI-powered career recommendation system that provides personalized career guidance based on your skills, education, work experience, and personality traits. It analyzes your resume, assesses your skills and interests using the RIASEC personality model, and recommends optimal career paths using machine learning. The system also identifies skill gaps, suggests upskilling courses, and shows which companies are actively hiring for your recommended roles with salary insights.
## Features
- Career exploration and role descriptions
- Personalized learning paths and resources
- Search and filtering for careers and skills
- Interactive RIASEC phycometric assessments

## Working
- **Resume Upload & Analysis**: Upload your resume (PDF format) and the system extracts skills, education, and work experience using NLP (Natural Language Processing).

 - **Skills Assessment**: Review and refine the auto-extracted skills from your resume. Add any additional skills manually.

 - **Personality Assessment**: Complete a RIASEC (Holland Code) personality assessment to understand your career interests across six dimensions: Realistic, Investigative, Artistic, Social, Enterprising, and Conventional.

 - **Career Recommendations**: An XGBoost machine learning model analyzes your profile and generates personalized career recommendations ranked by match percentage. Each recommendation includes:

- **Job role details from O*NET database**: Required skills, abilities, and knowledge, Average salary and education requirements, Top companies hiring for this role with location and salary data
- **Skill Gap Analysis**: Compare your current skills against the requirements for each recommended career to identify gaps.

- **Upskilling Recommendations**: Receive personalized course recommendations from platforms like Udemy, Coursera, and edX to bridge skill gaps.

## Tech stack

- *Frontend*: Streamlit
- *Machine Learning*: XGBoost, scikit-learn ( TF-IDF vectorization, label encoding, model evaluation)
- *Natural Language Processing*: spaCy, NLTK
- *Data Processing*: Pandas, NumPy
- *Visualization*: Plotly
- *Document Processing*: PyPDF2
- *Data Storage*: CSV Files

## Getting started

### Prerequisites
Install these tools as needed:
- Python Version: Python 3.11 or higher

Core Dependencies
- streamlit (>=1.45.0) - Web application framework
- xgboost (>=3.0.0) - Machine learning recommendation engine
- pandas (>=2.2.3) - Data manipulation and CSV handling
- numpy (>=2.2.5) - Numerical computing
- scikit-learn (>=1.6.1) - Machine learning utilities and preprocessing
- spacy (>=3.8.5) - Natural language processing for resume parsing
- nltk (>=3.9.1) - Text processing and tokenization
- pypdf2 (>=3.0.1) - PDF resume parsing
- plotly (>=6.0.1) - Interactive data visualizations
- Git

### Commands to Run Locally

**Step 1:** Clone the Repository `git clone https://github.com/your-username/career-compass.git`
`cd career-compass`

**Step 2:** Install Python Dependencies `pip install -r requirements.txt`

Or if using pyproject.toml with uv: `pip install -e` .

**Step 3:** Download spaCy Language Model `python -m spacy download en_core_web_sm`

**Step 4:** Download NLTK Data (Optional)
The app will download necessary NLTK data automatically on first run, but you can pre-download: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

**Step 5:** Run the Application `streamlit run app.py --server.port 5000`

**Step 6:** Access the Application, Open your browser and navigate to: `http://localhost:5000`


## Contributing
Thank you for considering contributing! A basic contributing workflow:
1. Fork the repository.
2. Create a branch: git checkout -b feature/your-feature
3. Commit your changes: git commit -m "feat: add ..."
4. Push to your fork: git push origin feature/your-feature
5. Open a pull request describing your changes.

## Roadmap
Planned improvements:
1. Improved career recommendation engine
2. OAuth sign-in and social login
3. Mobile responsive UI / PWA support
4. Import/export user plans
5. Analytics and reporting dashboard

Feel free to edit and expand this section to reflect real plans and milestones.

---
