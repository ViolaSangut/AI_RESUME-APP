import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import JobPosting, CandidateMatch
from .forms import JobPostingForm
from core.utils.matching_algorithm import JobMatchingAlgorithm
from resumes.models import Resume

# Configure logging
logger = logging.getLogger(__name__)

@login_required
def job_detail(request, pk):
    """
    Detailed view of a specific job posting
    """
    try:
        job = get_object_or_404(JobPosting, pk=pk)

        # Check if user has already applied or matched
        user_match = None
        if hasattr(request.user, 'resume'):
            user_match = CandidateMatch.objects.filter(
                job_posting=job,
                candidate=request.user
            ).first()

        context = {
            'job': job,
            'user_match': user_match
        }
        return render(request, 'jobs/job_detail.html', context)

    except Exception as e:
        logger.error(f"Job detail error: {e}")
        messages.error(request, "Unable to retrieve job details.")
        return redirect('job_list')

@login_required
def job_list(request):
    """
    Paginated and filterable job list
    """
    try:
        # Base queryset
        jobs_queryset = JobPosting.objects.all()

        # Search and filter
        search_query = request.GET.get('search', '')
        if search_query:
            jobs_queryset = jobs_queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Pagination
        paginator = Paginator(jobs_queryset, 10)  # 10 jobs per page
        page = request.GET.get('page', 1)

        try:
            jobs = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            jobs = paginator.page(1)

        context = {
            'jobs': jobs,
            'search_query': search_query,
            'total_jobs': jobs_queryset.count()
        }
        return render(request, 'jobs/job_list.html', context)

    except Exception as e:
        logger.error(f"Job list error: {e}")
        messages.error(request, "Unable to retrieve job listings.")
        return render(request, 'jobs/job_list.html', {'jobs': []})

@login_required
def job_create(request):
    """
    Job posting creation with enhanced validation
    """
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            try:
                job = form.save(commit=False)
                job.recruiter = request.user
                job.save()

                messages.success(request, "Job posting created successfully!")
                return redirect('job_list')

            except Exception as e:
                logger.error(f"Job creation error: {e}")
                messages.error(request, "Failed to create job posting.")
    else:
        form = JobPostingForm()

    return render(request, 'jobs/job_create.html', {'form': form})

@login_required
def match_candidates(request, job_id):
    """
    Advanced candidate matching with comprehensive error handling
    """
    try:
        # Fetch job with error handling
        job = get_object_or_404(JobPosting, id=job_id)

        # Verify user permissions
        if job.recruiter != request.user:
            messages.error(request, "You are not authorized to view matches for this job.")
            return redirect('job_list')

        # Fetch resumes with optional filtering
        resumes = Resume.objects.select_related('candidate')

        # Initialize matching algorithm
        matching_algo = JobMatchingAlgorithm()
        matches = []

        # Bulk create matches to reduce database queries
        candidate_matches = []

        for resume in resumes:
            try:
                # Calculate match score
                match_result = matching_algo.calculate_match_score(
                    resume.parsed_data,
                    job.description
                )

                # Create match object
                match = CandidateMatch(
                    job_posting=job,
                    candidate=resume.candidate,
                    match_score=match_result.get('overall_score', 0),
                    success_probability=match_result.get('overall_score', 0),
                    detailed_analysis=match_result
                )
                candidate_matches.append(match)

                # Prepare match data for display
                matches.append({
                    'candidate': resume.candidate,
                    'match_score': match_result.get('overall_score', 0),
                    'skills': match_result.get('matched_skills', [])
                })

            except Exception as e:
                logger.warning(f"Match calculation error for resume {resume.id}: {e}")

        # Bulk create matches
        CandidateMatch.objects.bulk_create(candidate_matches)

        # Sort matches by score
        matches.sort(key=lambda x: x['match_score'], reverse=True)

        # Pagination for matches
        paginator = Paginator(matches, 10)
        page = request.GET.get('page', 1)

        try:
            paginated_matches = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_matches = paginator.page(1)

        context = {
            'job': job,
            'matches': paginated_matches,
            'total_matches': len(matches)
        }

        return render(request, 'jobs/candidate_matches.html', context)

    except Exception as e:
        logger.error(f"Candidate matching error: {e}")
        messages.error(request, "Failed to process candidate matches.")
        return redirect('job_list')

@login_required
def candidate_match_detail(request, match_id):
    """
    Detailed view of a specific candidate match
    """
    try:
        match = get_object_or_404(
            CandidateMatch,
            id=match_id,
            job_posting__recruiter=request.user
        )

        context = {
            'match': match,
            'detailed_analysis': match.detailed_analysis
        }

        return render(request, 'jobs/candidate_match_detail.html', context)

    except Exception as e:
        logger.error(f"Candidate match detail error: {e}")
        messages.error(request, "Unable to retrieve match details.")
        return redirect('job_list')
