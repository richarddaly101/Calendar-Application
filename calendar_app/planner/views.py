from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.utils.safestring import mark_safe
from datetime import datetime as dt,timedelta
import datetime


# Create your views here.

def index(request):
    """Serve homepage page"""
    events = Event.objects.all()
    today = dt.today()
    year=today.year
    print(request.method)
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



#2020-11-15
def create(request):
    form = Create_Event(request.POST)
    if form.is_valid():
        #create http response object
        print("form valid")
        day=form.cleaned_data['day']
        note = form.cleaned_data['note']
        start=form.cleaned_data['start']
        end = form.cleaned_data['end']
        form.save()
        return redirect('/')
    else:
        return HttpResponse("""Error in form input, please try again""")

def update(request,event_id):
    event=Event.objects.get(id = event_id)
    if request.method == 'POST':
        form = Create_Event(request.POST, request.FILES, instance=event)
        if form.is_valid():
            print('valid in update')
            form.save()
            return redirect('/')
    #below if if GET request so just output form with fields filled
    else:
        form = Create_Event(instance=event)
        return render(request, 'update.html',context={'form':form,'event':event})



def delete(request,event_id):
    event=Event.objects.get(id = event_id)
    event.delete()
    return redirect('/')

