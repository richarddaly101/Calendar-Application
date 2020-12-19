from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.utils.safestring import mark_safe
from datetime import datetime as dt
from .models import Event
from django.db.models import Q



def index(request):
    """Serve homepage, every operation results in redirect to this page with updated database objects"""
    events = Event.objects.all()
    today = dt.today()
    year=today.year
    #if post method sent go to next month per user request
    if request.method == 'POST':
        month=request.POST.get('month')
        month=int(month)
        month+=1
        if month>12:
            month=1
        cal = Calendar(year, month)
    else:
        month=today.month
        cal=Calendar(year,month)
    calendar= mark_safe(cal.formatmonth(withyear=True))

    context = {
        'calendar':calendar,
        'events':events,
        'month':month
    }
    return render(request, 'index.html',context=context)



def create(request):
    """Function invoked when user wishes to create new event"""
    form = Create_Event(request.POST)
    if form.is_valid():
        #create http response object
        day=form.cleaned_data['day']
        note = form.cleaned_data['note']
        start=form.cleaned_data['start']
        end = form.cleaned_data['end']
        # Below checks if there is a time range overlap between user event and existing events in database
        time_filter = Q(start__lte=start) & Q(end__gte=end) | Q(start__gte=start) & Q(end__lte=end)
        # Check the day for time overlap
        filter_check = Event.objects.filter(time_filter, day__contains=day).exists()
        if filter_check == True:
            return HttpResponse("""Time slot already booked, please try again""")
        form.save()
        #redirect to homepage
        return redirect('/')
    else:
        return HttpResponse("""Error in times input, please try again""")

def update(request,event_id):
    """Function invoked when user updates an existing event"""
    event=Event.objects.get(id = event_id)
    if request.method == 'POST':
        form = Create_Event(request.POST, request.FILES, instance=event)
        if form.is_valid():
            print('valid in update')
            form.save()
            return redirect('/')
    #below if GET request received so just output form with fields filled
    else:
        form = Create_Event(instance=event)
        return render(request, 'update.html',context={'form':form,'event':event})



def delete(request,event_id):
    """Function invoked when user deletes an existing event"""
    event=Event.objects.get(id = event_id)
    event.delete()
    return redirect('/')

