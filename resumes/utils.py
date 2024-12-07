# resumes/utils.py
import os
import re

from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

def parse_resume(file_path):
    """
    Parse resume using LlamaParse
    """
    try:
        # Set up parser
        parser = LlamaParse(
            result_type="markdown"
        )

        # Configure file extractor
        file_extractor = {".pdf": parser}

        # Parse document
        documents = SimpleDirectoryReader(
            input_files=[file_path],
            file_extractor=file_extractor
        ).load_data()

        # Extract content from parsed document
        text = documents[0].text


        data  = {
            'skills': extract_skills(text),
            'experience': extract_experience(text),
            'education': extract_education(text),
            'raw_text': text
        }
        # print(data)
        return {
            'skills': extract_skills(text),
            'experience': extract_experience(text),
            'education': extract_education(text),
            'raw_text': text
        }
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return {}

def extract_skills(text):
    """
    Extract skills from resume text
    """
    # Predefined skill keywords
    skill_keywords = [
        # Technical Skills
        'python', 'django', 'flask', 'javascript', 'react', 'nodejs',
        'machine learning', 'data analysis', 'sql', 'git', 'html', 'css',
        'tensorflow', 'keras', 'aws', 'azure', 'cloud computing',
        'api development', 'devops', 'docker', 'kubernetes', 'big data',
        'data visualization', 'r', 'sas', 'excel', 'git', 'ruby',
        'c++', 'java', 'swift', 'typescript', 'graphql',
        # Cybersecurity Skills
        'network security', 'ethical hacking', 'digital marketing',
        'agile methodology', 'scrum', 'ux/ui design', 'management information systems',
        # Soft Skills
        'communication', 'leadership', 'teamwork', 'problem solving',
        'project management', 'time management', 'critical thinking',
        'adaptability', 'emotional intelligence', 'customer service', 'mentoring',
        # Industry-Specific Skills
        'financial analysis', 'regulatory compliance', 'supply chain management',
        'product development', 'market research', 'business analysis',
        'sales strategy', 'public speaking', 'branding',
        'healthcare management', 'educational technology', 'e-commerce',
        'mobile development', 'IoT (Internet of Things)', 'blockchain',
        # Emerging Skills
        'artificial intelligence', 'natural language processing', 'robotics',
        'quantum computing', 'virtual reality', 'augmented reality',
        'cybersecurity', 'machine learning ops (MLOps)', 'data engineering',
        'low-code development', 'no-code solutions', 'chatbot development'
    ]

    # Case-insensitive skill extraction
    skills = [
        skill for skill in skill_keywords
        if skill.lower() in text.lower()
    ]

    return list(set(skills))

def extract_experience(text):
    """
    Extract work experience details
    """
    # Experience patterns
    experience_patterns = [
        # Capture title, dates, and company (various formats)
        r'####\s*(?P<title>.+?)(?:\n|$)\s*(?P<dates>(?:\d{2}\/\d{4}-\d{2}\/\d{4}|\d{2}\/\d{4} to Current|\d{4}-\d{4}|\d{4}|\bPresent\b))\s*(?P<company>.+?)(?=---|\Z)',

        # Capture job responsibilities (allowing for different bullet point styles)
        r'-\s*(?P<responsibility>.+?)(?=\n-|\Z)',

        # Capture job responsibilities with numbering
        r'^\d+\.\s*(?P<responsibility>.+?)(?=\n\d+\.|\Z)',

        # Pattern for years of experience, accommodating various phrasing
        r'(\d+)\s*(?:years?|yrs?|yr|months?|mos?|weeks?|wks?)?\s*of\s*(?:experience|work)',

        # Capture multiple roles at the same company
        r'####\s*(?P<title>.+?)\s*at\s*(?P<company>.+?)\s*$(?P<dates>[^)]+)$',

        # Capture project specifics for roles
        r'### Projects\s*(?P<projects>(?:.+?\n?)+?)(?=\n###|\Z)',

        # Capture achievements or notable contributions
        r'### Achievements\s*(?P<achievements>(?:.+?\n?)+?)(?=\n###|\Z)',

        # Capture freelance or consulting experience
        r'####\s*Freelance:\s*(?P<title>.+?)\s*at\s*(?P<company>.+?)\s*(?P<dates>.+?)(?:\n|$)',
    ]

    experiences = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        experiences.extend(matches)

    return experiences

def extract_education(text):
    """
    Extract education information
    """
    # Education patterns
    education_patterns = [
    # Capture degree types (BS, MS, PhD), majors, institutions, and dates
    r'####\s*(?P<institution>.+?)\s*(?P<dates>\d{2}\/\d{4}-\d{2}\/\d{4}|\d{4}-\d{4}|\d{4})\s*(?P<degree>[B|M|D]?[a-zA-Z\s]+)(?:\s*$(?P<major>.+?)$)?(?:\n|$)',

    # Capture certification phrases and institutions
    r'####\s*(?P<institution>.+?)\s*(?P<dates>\d{4}-\d{4}|\d{4})\s*(?P<certificate>.+?)(?:\n|$)',

    # Capture general education descriptions in a "### EDUCATION" section
    r'### EDUCATION\s*([^#]+)',  # Capture everything under the education section

    # Capture online courses or specific training programs
    r'### ONLINE COURSES\s*(?P<course_name>.+?)\s*-\s*(?P<platform>.+?)\s*$(?P<dates>\d{4})$(?:\n|$)',

    # Capture high school education with dates and locations
    r'####\s*(?P<high_school>.+?)\s*(?P<high_school_dates>\d{4}-\d{4})(?:\s*$(?P<high_school_location>.+?)$)?(?:\n|$)',

    # Capture advanced degrees with honors or additional details
    r'####\s*(?P<institution>.+?)\s*(?P<dates>\d{4}-\d{4})\s*(?P<degree>.+?)\s*(?:$(?P<honors>.+?)$)?(?:\n|$)',

    # Capture associate degrees and technical certifications
    r'####\s*(?P<institution>.+?)\s*(?P<dates>\d{4}-\d{4})\s*(?P<degree>Associates|Certification|Diploma)\s*(?P<major>.+?)(?:\n|$)',

    # Capture graduation phrases without specific dates
    r'Graduated\s*(?P<degree>.+?)(?:\s*from\s*(?P<institution>.+?))?(\s*in\s*(?P<graduation_year>\d{4}))?(?:\n|$)',

    # Capture continuing education or professional development
    r'### CONTINUING EDUCATION\s*(?P<institution>.+?)\s*(?P<dates>\d{4}-\d{4}|\d{4})\s*(?P<course>.+?)(?:\n|$)',

    # Capture certifications with issuing organizations
    r'####\s*(?P<certificate>.+?)\s*$(?P<issuing_organization>.+?)$\s*(?P<certificate_dates>\d{4}-\d{4}|\d{4})(?:\n|$)',
]
    educations = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        educations.extend(matches)

    return educations
# parse_resume("/var/www/job_matching_system/temp_resume.pdf")
