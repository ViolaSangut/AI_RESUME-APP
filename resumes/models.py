from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser

class Resume(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    skills = models.JSONField(default=list)
    experience_years = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        null=True,  # Allow null
        blank=True  # Allow blank in forms
    )
    education = models.TextField(blank=True, null=True)
    parsed_data = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure experience_years is never negative
        if self.experience_years is None:
            self.experience_years = 0

        # Validate experience years
        self.experience_years = max(0, self.experience_years)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate.username}'s Resume"
