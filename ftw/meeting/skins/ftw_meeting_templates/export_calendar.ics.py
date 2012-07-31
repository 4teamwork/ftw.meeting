## Script (Python) "export_calendar.ics"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

PRODID = "-//Teamraum.ch//Event//EN"

# iCal header and footer
ICS_HEADER = """\
BEGIN:VCALENDAR
PRODID:%(prodid)s
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:office others
X-WR-TIMEZONE:Europe/Zurich
X-WR-CALDESC:
BEGIN:VTIMEZONE
TZID:Europe/Zurich
X-LIC-LOCATION:Europe/Zurich
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
"""

ICS_FOOTER = """\
END:VCALENDAR
"""
ppath = '/'.join(context.getPhysicalPath())


events = context.portal_catalog(portal_type='Meeting', path=ppath, start={'query' : context.ZopeTime() - 280, 'range' : 'min'})
utils = context.plone_utils
charset = utils.getSiteEncoding()
if context.REQUEST.form.get('plain','') != '1':
    context.REQUEST.RESPONSE.setHeader('Content-Type', 'text/calendar; charset=utf-8')
    context.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.ics"' % 'calendar_%s'%context.pretty_title_or_id())
print ICS_HEADER % { 'prodid' : PRODID, }

for event in events:
    print event.getObject().getICal()

print ICS_FOOTER

return printed
