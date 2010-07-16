"""Common configuration constants
"""

PROJECTNAME = 'ftw.meeting'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Meeting Item': 'ftw.meeting: Add Meeting Item',
    'Meeting': 'ftw.meeting: Add Meeting',
}

INDEXES = (("getAttendeesOrUsers", "KeywordIndex"),
          )
          
METADATA = ('getAttendeesOrUsers', )

product_globals = globals()
