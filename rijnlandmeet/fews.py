'''
Created on Jan 16, 2017

@author: theo
'''

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from acacia.data.models import Series
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_series_old(root,series):
    s = ET.SubElement(root,'series')
    h = ET.SubElement(s,'header')
    ET.SubElement(h,'type').text='instantaneous'
    ET.SubElement(h,'locationId').text=series.meetlocatie().name
    ET.SubElement(h,'parameterId').text='EC'
    ET.SubElement(h,'timeStep',{'unit': 'nonequidistant'})
    start = series.van().replace(microsecond=0)
    ET.SubElement(h,'startDate',{'date': str(start.date()),'time': str(start.time())})
    end = series.tot().replace(microsecond=0)
    ET.SubElement(h,'endDate',{'date': str(end.date()),'time': str(end.time())})
    ET.SubElement(h,'missVal').text='-999'
    ET.SubElement(h,'longName').text=series.name
    ET.SubElement(h,'units').text=series.unit
    for p in series.datapoints.all():
        date = p.date.replace(microsecond=0)
        ET.SubElement(s,'event',{'date':str(date.date()), 'time':str(date.time()), 'value': str(p.value)})
        
    return root

def add_series(root,series):

    loc = series.meetlocatie()
    
    s = ET.SubElement(root,'series')
    h = ET.SubElement(s,'header')
    ET.SubElement(h,'type').text='instantaneous'
    ET.SubElement(h,'locationId').text=str(loc.id)
    # parameter is something like EC, EC_diep, EC_ondiep etc...
    ET.SubElement(h,'parameterId').text=series.name
    ET.SubElement(h,'timeStep',{'unit': 'nonequidistant'})
    start = series.van().replace(microsecond=0)
    ET.SubElement(h,'startDate',{'date': str(start.date()),'time': str(start.time())})
    end = series.tot().replace(microsecond=0)
    ET.SubElement(h,'endDate',{'date': str(end.date()),'time': str(end.time())})
    ET.SubElement(h,'missVal').text='-999'
    ET.SubElement(h,'longName').text=unicode(loc.meetpunt.waarnemer)
    ET.SubElement(h,'stationName').text=unicode(loc)
    ET.SubElement(h,'units').text=series.unit
    ET.SubElement(h,'x').text='%.1f' % loc.location.x
    ET.SubElement(h,'y').text='%.1f' % loc.location.y
    z = loc.meetpunt.ahn or loc.location.z
    if z:
        ET.SubElement(h,'z').text='%.1f' % z

    ll = loc.latlon()
    ET.SubElement(h,'lon').text='%.8f' % ll.x
    ET.SubElement(h,'lat').text='%.8f' % ll.y
    
    for p in series.datapoints.all():
        date = p.date.replace(microsecond=0)
        ET.SubElement(s,'event',{'date':str(date.date()), 'time':str(date.time()), 'value': str(p.value)})
        
    return root
    
# convert acaciadata timeseries to FEWS published interface format
def series_as_pi(series):
    root = ET.Element('TimeSeries',
                {'xmlns':'http://www.wldelft.nl/fews/PI',
                 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                 'xmlns:xlink':'http://www.w3.org/1999/xlink', 
                 'xsi:schemaLocation':'http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd',
                 'version':'1.2'
    })
    ET.SubElement(root, 'timezone').text='0.0'
    
    if isinstance(series, Series):
        add_series(root,series)
    else:
        # probably collection of series
        for s in series:
            add_series(root, s)

    return ET.ElementTree(root)

def test():
    import sys
    from acacia.data.models import Series
    s = Series.objects.first()
    tree = series_as_pi(s)
    tree.write(sys.stdout)
