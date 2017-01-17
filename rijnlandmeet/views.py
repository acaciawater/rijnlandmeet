'''
Created on Jan 16, 2017

@author: theo
'''
from django.shortcuts import get_object_or_404
from acacia.data.models import Series
from fews import series_as_pi
from django.http.response import HttpResponse
from StringIO import StringIO
from django.utils.text import slugify
def to_fews(request,pk=None):

    if pk is None:
        queryset = Series.objects.all()
        series = queryset.first()
        filename = slugify(series.project().name)+'.xml'
    else:
        queryset = Series.objects.filter(pk=pk)
        series = queryset.first()
        filename = slugify(unicode(series))+'.xml'
    tree = series_as_pi(queryset)
    io = StringIO()
    tree.write(io)
    resp = HttpResponse(io.getvalue(), content_type='application/xml')
    resp['Content-Disposition'] = 'inline; filename=%s' % filename
    return resp
