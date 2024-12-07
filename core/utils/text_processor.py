import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        # Download NLTK resources with comprehensive error handling
        self._download_nltk_resources()

        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except Exception as e:
            logger.error(f"Error initializing NLTK components: {e}")
            self.stop_words = set()
            self.lemmatizer = None

    def _download_nltk_resources(self):
        """
        Download NLTK resources with comprehensive error handling
        """
        resources = [
            ('punkt', 'Tokenization'),
            ('stopwords', 'Stop Words'),
            ('wordnet', 'Lemmatization')
        ]

        for resource, description in resources:
            try:
                nltk.download(resource, quiet=True)
                logger.info(f"Successfully downloaded {description} resource")
            except Exception as e:
                logger.warning(f"Failed to download {description} resource: {e}")

    def preprocess_text(self, text):
        """
        Comprehensive text preprocessing method

        :param text: Input text to preprocess
        :return: Preprocessed text as a string
        """
        if not text:
            return ''

        try:
            # Lowercase and tokenize
            tokens = word_tokenize(text.lower())

            # Remove stopwords and lemmatize
            cleaned_tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token.isalnum() and token not in self.stop_words
            ]

            return ' '.join(cleaned_tokens)

        except Exception as e:
            logger.error(f"Text preprocessing error: {e}")
            return text.lower()

    def calculate_similarity(self, text1, text2, method='cosine'):
        """
        Calculate text similarity using different methods

        :param text1: First text
        :param text2: Second text
        :param method: Similarity calculation method
        :return: Similarity score
        """
        if not text1 or not text2:
            return 0.0

        try:
            if method == 'cosine':
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([
                    self.preprocess_text(text1),
                    self.preprocess_text(text2)
                ])
                return cosine_similarity(tfidf_matrix)[0][1]
            elif method == 'jaccard':
                # Jaccard similarity
                set1 = set(self.preprocess_text(text1).split())
                set2 = set(self.preprocess_text(text2).split())

                intersection = len(set1.intersection(set2))
                union = len(set1.union(set2))

                return (intersection / union if union > 0 else 0.0) 

            else:
                logger.warning(f"Unsupported similarity method: {method}")
                return 0.0

        except Exception as e:
            logger.error(f"Similarity calculation error: {e}")
            return 0.0

    def extract_skills(self, text, custom_skills=None):
        """
        Extract skills from text

        :param text: Input text to extract skills from
        :param custom_skills: Optional custom list of skills
        :return: List of extracted skills
        """
        if not text:
            return []

        # Default skill list
        default_skills = [
            # Programming Languages
    'python', 'javascript', 'java', 'c#', 'c++', 'c', 'ruby', 'go',
    'swift', 'scala', 'typescript', 'html', 'css', 'bash', 'sql',

    # Web Development Frameworks
    'django', 'flask', 'react', 'angular', 'vue.js', 'bootstrap',
    'node.js', 'express.js', 'spring', 'ruby on rails', 'laravel',

    # Mobile Development
    'android development', 'ios development', 'react native',
    'flutter', 'cordova', 'xamarin',

    # Database Technologies
    'mysql', 'postgresql', 'mongodb', 'cassandra', 'redis',
    'sqlite', 'oracle', 'nosql', 'bigtable',

    # Cloud Platforms
    'aws', 'azure', 'google cloud platform', 'ibm cloud',
    'heroku', 'digital ocean', 'linode',

    # DevOps & CI/CD
    'docker', 'kubernetes', 'jenkins', 'travis ci', 'circleci',
    'ansible', 'puppet', 'chef', 'terraform',

    # Version Control & Collaboration
    'git', 'github', 'gitlab', 'bitbucket', 'svn',

    # Data Science & Analytics
    'machine learning', 'deep learning', 'data visualization',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow',
    'keras', 'matplotlib', 'seaborn',

    # Business Intelligence Tools
    'tableau', 'power bi', 'looker', 'google data studio',

    # Cybersecurity Tools & Concepts
    'penetration testing', 'network security', 'firewall',
    'siem', 'intrusion detection', 'cryptography',

    # Networking
    'tcp/ip', 'dns', 'http/https', 'vpn', 'routing protocols',
    'network troubleshooting', 'wireshark',

    # Emerging Technologies
    'artificial intelligence', 'natural language processing',
    'blockchain', 'internet of things (IoT)',
    'augmented reality', 'virtual reality',

    # Software Development Methodologies
    'agile', 'scrum', 'kanban', 'test-driven development (TDD)',
    'continuous integration', 'continuous deployment',

    # Other Tools & Technologies
    'elasticsearch', 'apache kafka', 'redis', 'apache hive',
    'spark', 'big data', 'hadoop',

    # Miscellaneous Technologies
    'graphql', 'socket programming', 'raspberry pi', 'arduino',
    '3D modeling software', 'ui/ux design principles'
     # Technical Skills
    'python', 'django', 'flask', 'javascript', 'react', 'angular', 'vue.js',
    'node.js', 'typescript', 'html', 'css', 'bootstrap', 'jQuery',
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'tensorflow',
    'keras', 'pytorch', 'openai', 'scikit-learn', 'pandas',
    'numpy', 'data visualization', 'matplotlib', 'seaborn',
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform',
    'jenkins', 'ci/cd', 'git', 'github', 'bitbucket',
    'machine learning', 'data analysis', 'big data', 'hadoop',
    'spark', 'elasticsearch', 'graphql', 'api development',
    'microservices', 'serverless architecture', 'restful services',

    # Cybersecurity Skills
    'network security', 'penetration testing', 'incident response',
    'firewall management', 'vulnerability assessment', 'security information and event management (SIEM)',

    # DevOps Skills
    'ansible', 'puppet', 'chef', 'monitoring', 'logging', 'performance tuning',

    # Soft Skills
    'communication', 'leadership', 'teamwork', 'problem solving',
    'project management', 'time management', 'critical thinking',
    'adaptability', 'creativity', 'emotional intelligence',
    'conflict resolution', 'negotiation', 'customer service',
    'mentoring', 'collaboration',

    # Emerging Technologies
    'artificial intelligence', 'natural language processing', 'robotics',
    'computer vision', 'augmented reality', 'virtual reality',
    'blockchain', 'internet of things (IoT)', 'quantum computing',

    # Industry-Specific Skills
    'financial analysis', 'market research', 'regulatory compliance',
    'business analysis', 'sales strategy', 'public speaking',
    'branding', 'healthcare management', 'educational technology',
    'e-commerce', 'mobile development', 'supply chain management',
    'product development'
        ]

        # Use custom skills if provided, otherwise use default
        skill_keywords = custom_skills or default_skills

        try:
            processed_text = self.preprocess_text(text)

            # Find matching skills (case-insensitive)
            found_skills = [
                skill for skill in skill_keywords
                if skill.lower() in processed_text
            ]

            return list(set(found_skills))

        except Exception as e:
            logger.error(f"Skill extraction error: {e}")
            return []

    def extract_keywords(self, text, top_n=10):
        """
        Extract top keywords from text

        :param text: Input text
        :param top_n: Number of top keywords to return
        :return: List of top keywords
        """
        if not text:
            return []

        try:
            # Preprocess and tokenize text
            processed_text = self.preprocess_text(text)

            # Tokenization: Use regex to find words, ignoring punctuation
            tokens = re.findall(r'\b\w+\b', processed_text.lower())  # Normalize to lowercase

            # Remove common stop words (you may extend this list)
            stop_words = set([
                'the', 'and', 'is', 'in', 'to', 'a', 'that', 'of',
                'it', 'on', 'for', 'with', 'as', 'are', 'this',
                'but', 'by', 'an', 'be', 'at', 'from', 'or', 'about',
                'has', 'have', 'had', 'will', 'would', 'should',
                'can', 'could', 'may', 'might', 'must', 'being',
                'which', 'who', 'what', 'when', 'where', 'why',
                'also', 'than', 'such', 'like', 'just', 'other',
                'more', 'some', 'any', 'these', 'those', 'both',
                'few', 'many', 'several', 'last', 'first', 'next',
                'previous', 'now', 'there', 'here', 'above', 'below',
                'along', 'between', 'during', 'after', 'before',
                'job', 'position', 'experience', 'responsibilities',
                'skills', 'development', 'training', 'achievements',
                'education', 'overview', 'summary', 'objective',
                'interests', 'awards', 'certifications', 'technical',
                'proficient', 'effective', 'demonstrated', 'strong',
                'ability', 'expertise'
            ])


            # Filter tokens to remove stop words and single-character tokens
            filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 1]

            # Count token frequencies
            keyword_freq = Counter(filtered_tokens)

            # Return top N keywords
            return [keyword for keyword, _ in keyword_freq.most_common(top_n)]

        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []
    def anonymize_text(self, text, replacement='[REDACTED]'):
        """
        Anonymize sensitive information in text

        :param text: Input text
        :param replacement: Replacement text for sensitive information
        :return: Anonymized text
        """
        if not text:
            return ''

        try:
            # Regex patterns for sensitive information
            patterns = [
    # Email - more complex formats including subdomains, special characters, and newer TLDs
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}+',  # Regex to handle multiple TLDs

    # Phone - handles a variety of formats including international, extension numbers, and special characters
    r'(?:(?:\+\d{1,3}[-. ]?)?$?\d{1,4}?$?[-. ]?\d{1,4}[-. ]?\d{1,4}(?:[-. ]?(?:#|ext\.?|x)\d+)?|(?:\+\d{1,3})?\d{1,4}[-. ]?\d{1,9})',

    # IP Address - handles both IPv4 and IPv6, including CIDR notation
    r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}|:(?::[0-9a-fA-F]{1,4}){1,7}|::(?:ffff:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|::(?:ffff:[0-9a-fA-F]{1,4}:){1,4}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
]

            anonymized_text = text
            for pattern in patterns:
                anonymized_text = re.sub(pattern, replacement, anonymized_text)

            return anonymized_text

        except Exception as e:
            logger.error(f"Text anonymization error: {e}")
            return text
