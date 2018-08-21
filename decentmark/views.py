from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect

from decentmark.forms import UnitForm
from decentmark.models import Unit


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