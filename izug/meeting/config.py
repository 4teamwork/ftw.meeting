"""Common configuration constants
"""

PROJECTNAME = 'izug.meeting'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Meeting Item': 'izug.meeting: Add Meeting Item',
    'Meeting': 'izug.meeting: Add Meeting',
}

INDEXES = (("getAttendeesOrUsers", "KeywordIndex"),
          )
          
METADATA = ('getAttendeesOrUsers', )

product_globals = globals()
