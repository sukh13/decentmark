from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from decentmark.forms import UnitForm, AssignmentForm, SubmissionForm, FeedbackForm
from decentmark.models import Unit, Assignment, Submission


@login_required
def unit_list(request) -> HttpResponse:
    """
    Unit List - List of units. Staff see all units. Non-staff see units they are enrolled in.
    """

    # Staff
    if request.user.is_staff:
        unit_list = Unit.objects.all().order_by('name')
    else:
        unit_list = Unit.objects.filter(user=request.user).order_by('name')

    unit_count = unit_list.count()

    context = {
        "unit_list": unit_list,
        "unit_count": unit_count,
    }

    return render(request, 'decentmark/unit_list.html', context)


@login_required
def unit_create(request) -> HttpResponse:
    """
    Unit Create - Create a new Unit
    """
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm()

    return render(request, 'decentmark/unit_create.html', {'form': form})


@login_required
def unit_edit(request, unit_id=None) -> HttpResponse:
    """
    Unit Create - Create a new Unit
    """

    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm(instance=unit)

    context = {
        'form': form,
        'unit': unit,
    }

    return render(request, 'decentmark/unit_edit.html', context)


@login_required()
def unit_view(request, unit_id=None) -> HttpResponse:
    """
    Unit View - View unit details
    """
    unit = get_object_or_404(Unit, id=unit_id)

    context = {
        "unit": unit,
    }

    return render(request, 'decentmark/unit_view.html', context)


@login_required
def assignment_create(request, unit_id=None) -> HttpResponse:
    """
    Assignment Create - Create a new Assignment
    """
    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.unit = unit
            form.save()
            return redirect(reverse('decentmark:assignment_list', args=(unit.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm()

    context = {
        'form': form,
        'unit': unit,
    }

    return render(request, 'decentmark/assignment_create.html', context)


@login_required
def assignment_edit(request, assignment_id=None) -> HttpResponse:
    """
    Assignment Edit - Edit an existing Assignment
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    unit = assignment.unit

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect(reverse('decentmark:assignment_list', args=(unit.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm(instance=assignment)

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
    }

    return render(request, 'decentmark/assignment_edit.html', context)


@login_required
def assignment_list(request, unit_id=None) -> HttpResponse:
    """
    Assignment List - List of assignments.
    Staff see all assignments. Non-staff see open assignments.
    """

    unit = get_object_or_404(Unit, id=unit_id)

    # Staff
    if request.user.is_staff:
        assignment_list = Assignment.objects.filter(unit=unit).order_by('start')
    else:
        # TODO: Filter by start > today
        assignment_list = Assignment.objects.filter(unit=unit).order_by('start')

    assignment_count = assignment_list.count()

    context = {
        "unit": unit,
        "assignment_list": assignment_list,
        "assignment_count": assignment_count,
    }

    return render(request, 'decentmark/assignment_list.html', context)


@login_required()
def assignment_view(request, assignment_id=None) -> HttpResponse:
    """
    Assignment View - View assignment details
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    unit = assignment.unit

    context = {
        "unit": unit,
        "assignment": assignment,
    }

    return render(request, 'decentmark/assignment_view.html', context)


@login_required
def submission_list(request, assignment_id=None) -> HttpResponse:
    """
    Submission List - List of submissions.
    Staff see all submissions. Non-staff see their own submissions.
    """

    assignment = get_object_or_404(Assignment, id=assignment_id)
    unit = assignment.unit

    # Staff
    if request.user.is_staff:
        submission_list = Submission.objects.filter(assignment=assignment).order_by('date')
    else:
        # TODO: Filter by user = request.user
        submission_list = Submission.objects.filter(assignment=assignment).order_by('date')

    context = {
        "unit": unit,
        "assignment": assignment,
        "submission_list": submission_list,
    }

    return render(request, 'decentmark/submission_list.html', context)


@login_required
def submission_create(request, assignment_id=None) -> HttpResponse:
    """
    Submission Create - Make a submission
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    unit = assignment.unit

    if request.method == 'POST':
        form = SubmissionForm(request.POST, initial={
            'assignment': assignment,
        })
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.user = request.user
            new_submission.assignment = assignment
            form.save()
            return redirect(reverse('decentmark:assignment_view', args=(assignment.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = SubmissionForm()

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
    }

    return render(request, 'decentmark/submission_create.html', context)


@login_required()
def submission_view(request, submission_id=None) -> HttpResponse:
    """
    Submission View - View submission details
    """
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    unit = assignment.unit

    context = {
        "unit": unit,
        "assignment": assignment,
        "submission": submission,
    }

    return render(request, 'decentmark/submission_view.html', context)


@login_required
def submission_mark(request, submission_id=None) -> HttpResponse:
    """
    Submission Mark - Mark a submission
    """
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    unit = assignment.unit

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=submission)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.marked = True
            form.save()
            return redirect(reverse('decentmark:submission_view', args=(submission.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = FeedbackForm(instance=submission)

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
        'submission': submission,
    }

    return render(request, 'decentmark/submission_mark.html', context)
