from django.db import models
from datetime import date
from calendar import HTMLCalendar

# Create your models here.
class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event',blank=False)
    note = models.TextField(u'Textual Notes', help_text=u'Notes', blank=False)
    start = models.TimeField(u'Starting time', help_text=u'Starting time',blank=False)
    end = models.TimeField(u'Final time', help_text=u'Final time',blank=False)


    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Event._meta.fields]

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    #The below functions used to format the structure of the calendar and how events appear in this was referenced
    #from https: // github.com / huiwenhw / django - calendar / tree / master / cal
    def formatday(self, day, events):
        events_per_day = events.filter(day__day=day)

        data = ''
        for event in events_per_day:
            data += f'<li> {event.note} {event.start} {event.end} </li>'
            id=event.id
            data += f'<li><a href = "/update/'+str(id)+'" ><p>Update Record</p></li>'
            data += f'<li><a href = "/delete/'+str(id)+'" ><p>Delete Record</p></li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {data} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        #filter events to populate in the calender by their respective month value
        events = Event.objects.filter(day__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal



