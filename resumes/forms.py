import os  # Add this import at the top of the file
from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    file = forms.FileField(
        label='Upload Resume',
        help_text='Supported formats: PDF, DOCX, DOC',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Resume
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            # Validate file type
            valid_extensions = ['.pdf', '.docx', '.doc']
            ext = os.path.splitext(file.name)[1].lower()

            if ext not in valid_extensions:
                raise forms.ValidationError('Unsupported file format. Please upload PDF, DOCX, or DOC.')

            # Optional: Validate file size (e.g., max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 5MB.')

        return file
