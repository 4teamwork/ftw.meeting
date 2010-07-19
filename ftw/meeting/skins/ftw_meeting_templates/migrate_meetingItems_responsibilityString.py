## Script (Python) "migrate_meetingItems_responsibilityString"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
meetingitems = context.portal_catalog({'portal_type':['Meeting Item']})

for item in meetingitems:
  try:
    obj = item.getObject()
    obj.setResponsibilityString(value="ischegau")
    obj.reindexObject()
    print "Item edited: %s - %s" % (item.Title, item.getPath())
  except:
    try:
      print "XXX - failed to edit: %s - %s" % (item.Title, item.getPath())
    except:
      print "Object with id %s seems to be broken" % item.id



return printed
