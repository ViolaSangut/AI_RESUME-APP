from django import forms
from .models import JobPosting

class JobPostingForm(forms.ModelForm):
    required_skills = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter skills separated by comma'})
    )

    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'required_skills', 'min_experience', 'salary_range']

    def clean_required_skills(self):
        skills = self.cleaned_data['required_skills']
        return [skill.strip() for skill in skills.split(',')]
