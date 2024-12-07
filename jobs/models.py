from django.db import models
from accounts.models import CustomUser

class JobPosting(models.Model):
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    min_experience = models.IntegerField()
    salary_range = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CandidateMatch(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    match_score = models.FloatField()
    success_probability = models.FloatField()
    detailed_analysis = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.candidate.username} - {self.job_posting.title}"
