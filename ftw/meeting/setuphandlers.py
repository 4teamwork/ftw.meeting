from Products.CMFCore.utils import getToolByName
from ftw.meeting.config import INDEXES, METADATA
from Products.ZCatalog.Catalog import CatalogError

def add_indexes(site):
    """Add our indexes to the catalog.

    Doing it here instead of in profiles/default/catalog.xml means we
    do not need to reindex those indexes after every reinstall.
    """

    context = site.getSite()
    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    
    
    for name, meta_type in INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
        if name in METADATA:
            try:
                catalog.manage_addColumn(name)
            except CatalogError:
                pass
