# resumes/views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import ResumeUploadForm
from .models import Resume
from .utils import parse_resume  # Local import
from core.utils.text_processor import TextProcessor
from jobs.models import JobPosting

logger = logging.getLogger(__name__)

@login_required
def resume_upload(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create resume instance
                resume = form.save(commit=False)
                resume.candidate = request.user


                # Save uploaded file locally
                uploaded_file = request.FILES['file']
                file_path = f'temp_resumes/{uploaded_file.name}'
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Parse resume using local file path
                parsed_data = parse_resume(file_path)
                # print(file_path)


                # Parse the uploaded resume
                # parsed_data = parse_resume(request.FILES['file'])

                # print(parsed_data)

                # Initialize text processor
                text_processor = TextProcessor()

                # Enhanced parsing
                resume_text = parsed_data.get('raw_text', '')

                # Extract additional insights
                parsed_data.update({
                    'skills': text_processor.extract_skills(resume_text),
                    'keywords': text_processor.extract_keywords(resume_text),
                })

                # Save parsed data
                resume.parsed_data = parsed_data
                resume.skills= parsed_data.get("skills")
                resume.education = parsed_data.get('education')
                resume.experience = parsed_data.get('experience')
                resume.save()

                # Find matching jobs
                matching_jobs = find_matching_jobs(resume, text_processor)

                messages.success(
                    request,
                    f'Resume uploaded successfully. Found {len(matching_jobs)} potential job matches.'
                )
                return redirect('resume_analysis', resume_id=resume.id)

            except Exception as e:
                logger.error(f"Resume upload error: {str(e)}", exc_info=True)
                messages.error(request, f'Error processing resume: {str(e)}')

    else:
        form = ResumeUploadForm()

    return render(request, 'resumes/resume_upload.html', {'form': form})
def find_matching_skills(resume_skills, job_skills):
    """
    Find matching skills with fuzzy matching and variations

    :param resume_skills: List of skills from resume
    :param job_skills: List of required job skills
    :return: List of matched skills
    """
    matched_skills = []

    for resume_skill in resume_skills:
        for job_skill in job_skills:
            # Normalize skills for comparison
            resume_skill_lower = resume_skill.lower()
            job_skill_lower = job_skill.lower()

            # Exact match (case-insensitive)
            if resume_skill_lower == job_skill_lower:
                matched_skills.append(resume_skill)
                break

            # Partial match
            elif (resume_skill_lower in job_skill_lower or
                  job_skill_lower in resume_skill_lower):
                matched_skills.append(resume_skill)
                break

            # Skill variations and common abbreviations
            skill_variations = [
                resume_skill_lower,
                resume_skill.replace('.js', ''),
                resume_skill.replace('js', ''),
                job_skill_lower,
                job_skill.replace('.js', ''),
                job_skill.replace('js', '')
            ]

            if any(
                var1 in var2 or var2 in var1
                for var1 in skill_variations
                for var2 in skill_variations
            ):
                matched_skills.append(resume_skill)
                break

    return list(set(matched_skills))  # Remove duplicates
def find_matching_jobs(resume, text_processor=None):
    """
    Find matching jobs based on resume content
    """
    if not text_processor:
        text_processor = TextProcessor()

    # Get resume skills and keywords
    print(resume.parsed_data)
    resume_skills = resume.parsed_data.get('skills', [])
    resume_keywords = resume.parsed_data.get('keywords', [])
    resume_text = resume.parsed_data.get('raw_text', '')

    # Build complex query
    job_query = Q()

    # Match skills
    for skill in resume_skills:
        job_query |= Q(description__icontains=skill)

    # Match keywords
    for keyword in resume_keywords:
        job_query |= Q(description__icontains=keyword)

    # Find potential jobs
    potential_jobs = JobPosting.objects.filter(job_query).distinct()

    # Rank jobs by similarity
    ranked_jobs = []
    for job in potential_jobs:
        # print(job.description)
        # Calculate similarity score
        similarity_score = text_processor.calculate_similarity(
            resume_text,
            job.description
        )

        ranked_jobs.append({
            'job': job,
            'similarity_score': similarity_score * 100,
            'matched_skills':  find_matching_skills(resume_skills, job.required_skills)


        })

    # Sort jobs by similarity score in descending order
    ranked_jobs.sort(key=lambda x: x['similarity_score'], reverse=True)

    return ranked_jobs

@login_required
def resume_analysis(request, resume_id):
    try:
        # Fetch resume with error handling
        resume = get_object_or_404(Resume, id=resume_id, candidate=request.user)

        # Initialize text processor
        text_processor = TextProcessor()

        # Find matching jobs
        matching_jobs = find_matching_jobs(resume, text_processor)

        context = {
            'resume': resume,
            'job_matches': matching_jobs,
            'skills': resume.parsed_data.get('skills', []),
            'keywords': resume.parsed_data.get('keywords', []),
            'ORIGINAL': resume.parsed_data,
            'raw_text_preview': resume.parsed_data.get('raw_text', '')
        }

        return render(request, 'resumes/resume_analysis.html', context)

    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}", exc_info=True)
        messages.error(request, 'Error analyzing resume.')
        return redirect('resume_upload')

@login_required
def resume_list(request):
    # Fetch user's resumes with basic information
    resumes = Resume.objects.filter(candidate=request.user).order_by('-id')

    return render(request, 'resumes/resume_list.html', {
        'resumes': resumes,
        'total_resumes': resumes.count()
    })

@login_required
def resume_delete(request, resume_id):
    try:
        # Fetch and delete resume with error handling
        resume = get_object_or_404(Resume, id=resume_id, candidate=request.user)
        resume.delete()

        messages.success(request, 'Resume deleted successfully.')
    except Exception as e:
        logger.error(f"Resume deletion error: {str(e)}", exc_info=True)
        messages.error(request, 'Error deleting resume.')

    return redirect('resume_list')



@login_required
def resume_matches_overview(request):
    # Fetch all resumes for the user
    resumes = Resume.objects.filter(candidate=request.user).order_by('-id')

    # Initialize text processor
    text_processor = TextProcessor()

    # Get matches for all resumes
    all_resume_matches = []
    for resume in resumes:
        matches = find_matching_jobs(resume, text_processor)
        all_resume_matches.append({
            'resume': resume,
            'matches': matches
        })

    return render(request, 'resumes/resume_matches_overview.html', {
        'all_resume_matches': all_resume_matches
    })
