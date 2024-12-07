from .text_processor import TextProcessor

class JobMatchingAlgorithm:
    def __init__(self):
        self.text_processor = TextProcessor()

    def calculate_match_score(self, resume_data, job_description):
        # Skill matching
        resume_skills = set(resume_data.get('skills', []))
        job_skills = set(self._extract_job_skills(job_description))
        skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills) if job_skills else 0

        # Text similarity
        text_similarity = self.text_processor.calculate_similarity(
            resume_data.get('processed_text', ''),
            job_description
        )

        # Experience matching
        resume_exp = resume_data.get('experience_years', 0)
        job_min_exp = self._extract_min_experience(job_description)
        experience_match = min(1.0, resume_exp / job_min_exp) if job_min_exp > 0 else 0

        # Weighted score calculation
        match_score = (
            skill_match * 0.6 +
            text_similarity * 0.2 +
            experience_match * 0.2
        )

        return {
            'overall_score': match_score * 100,
            'skill_match': skill_match * 100,
            'text_similarity': text_similarity * 100,
            'experience_match': experience_match * 100
        }

    def _extract_job_skills(self, job_description):
        return self.text_processor.extract_skills(job_description)

    def _extract_min_experience(self, job_description):
        matches = re.findall(r'(\d+)\s*(?:year|yr)\s*experience', job_description, re.IGNORECASE)
        return int(matches[0]) if matches else 0
