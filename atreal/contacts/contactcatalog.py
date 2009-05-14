from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_parent
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.ObjectManager import ObjectManager
from Globals import InitializeClass, DTMLFile, PersistentMapping
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore import permissions
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCatalog.Catalog import Catalog
from Products import CMFCore
import os.path
from zope.interface import implements

from interfaces import IContactCatalog

CONTACT_CATALOG = "portal_contacts"

_www = os.path.join(os.path.dirname(__file__), 'www')
_catalog_dtml = os.path.join(os.path.dirname(CMFCore.__file__), 'dtml')




class IndexableObjectWrapper(object):
    """Wrapper for object indexing
    """    
    def __init__(self, obj):
        self._obj = obj
                
    def __getattr__(self, name):
        return getattr(self._obj, name)
        
    def Title(self):
        # TODO: dumb try to make sure UID catalog doesn't fail if Title can't be
        # converted to an ascii string
        # Title is used for sorting only, maybe we could replace it by a better
        # version
        title = self._obj.Title()
        try:
            return str(title)
        except UnicodeDecodeError:
            return self._obj.getId()
    
    def sortable_title(self):
        return self.Title()


class ContactCatalog(UniqueObject, ZCatalog):
    """Reference catalog
    """

    id = CONTACT_CATALOG
    security = ClassSecurityInfo()
    implements(IContactCatalog)

    manage_catalogFind = DTMLFile('catalogFind', _catalog_dtml)
    manage_options = ZCatalog.manage_options

    # XXX FIXME more security

    manage_options = ZCatalog.manage_options + \
        ({'label': 'Rebuild catalog',
         'action': 'manage_rebuildCatalog',}, )

    def __init__(self, id=CONTACT_CATALOG, title='', vocab_id=None, container=None):
        """We hook up the brains now"""
        ZCatalog.__init__(self, id, title, vocab_id, container)
        #self._catalog = ReferenceBaseCatalog()

    # we probably have to override some classes to handle contacts
     
    
InitializeClass(ContactCatalog)
