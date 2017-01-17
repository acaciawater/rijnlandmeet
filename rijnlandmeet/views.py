'''
Created on Jan 16, 2017

@author: theo
'''
from django.shortcuts import get_object_or_404
from acacia.data.models import Series
from iom.models import Waarnemer, Meetpunt
from fews import series_as_pi
from django.http.response import HttpResponse
from StringIO import StringIO
from django.utils.text import slugify

def series_to_fews(queryset, filename):
    tree = series_as_pi(queryset)
    io = StringIO()
    tree.write(io)
    resp = HttpResponse(io.getvalue(), content_type='application/xml')
    resp['Content-Disposition'] = 'attachment; filename=%s' % filename
    return resp
    
def to_fews(request,pk=None):

    if pk is None:
        queryset = Series.objects.all()
        series = queryset.first()
        filename = slugify(series.project().name)+'.xml'
    else:
        queryset = Series.objects.filter(pk=pk)
        series = queryset.first()
        filename = slugify(unicode(series))+'.xml'

    return series_to_fews(queryset, filename)

def waarnemer_to_fews(request, pk):
    waarnemer = get_object_or_404(Waarnemer,pk=pk)
    meetpunten = waarnemer.meetpunt_set.all()
    series = [s for m in meetpunten for s in m.series()]
    filename = slugify(unicode(waarnemer))+'.xml'
    return series_to_fews(series, filename)

def meetpunt_to_fews(request, pk):
    meetpunt = get_object_or_404(Meetpunt,pk=pk)
    filename = slugify(unicode(meetpunt))+'.xml'
    return series_to_fews(meetpunt.series(), filename)