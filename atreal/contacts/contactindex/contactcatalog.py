from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_parent
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import search_zcatalog as SearchZCatalog
from Globals import InitializeClass, DTMLFile
from Products.CMFCore.utils import UniqueObject
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCatalog.Catalog import Catalog
from Products import CMFCore
import os.path

from zope.interface import implements
from zope.interface.declarations import ObjectSpecificationDescriptor


from interfaces import IContactCatalog, IIndexableObjectWrapper
from atreal.contacts.interfaces import IContactIndex
from atreal.contacts.config import CONTACT_CATALOG
#from plone.contacting.interfaces import IContactManager

_www = os.path.join(os.path.dirname(__file__), 'www')
_catalog_dtml = os.path.join(os.path.dirname(CMFCore.__file__), 'dtml')

class IndexableObjectSpecification(ObjectSpecificationDescriptor):

    def __get__(self, inst, cls=None):
        if inst is None:
            return getObjectSpecification(cls)
        else:
            provided = providedBy(inst._IndexableObjectWrapper__ob)
            cls = type(inst)
            return ObjectSpecification(provided, cls)
            


class IndexableObjectWrapper(object):

    implements(IIndexableObjectWrapper)
    __providedBy__ = IndexableObjectSpecification()

    def __init__(self, vars, ob):
        self.__vars = vars
        self.__ob = ob

    def __str__(self):
        try:
            # __str__ is used to get the data of File objects
            return self.__ob.__str__()
        except AttributeError:
            return object.__str__(self)

    def __getattr__(self, name):
        vars = self.__vars
        if vars.has_key(name):
            return vars[name]
        return getattr(self.__ob, name)
        
    def path(self):
        """return the path"""
        return self.__ob.aq_parent.getPhysicalPath()


class ContactCatalog(UniqueObject, ZCatalog):
    """Reference catalog
    """

    id = CONTACT_CATALOG
    security = ClassSecurityInfo()
    implements(IContactCatalog)

    manage_catalogFind = DTMLFile('catalogFind', _catalog_dtml)
    manage_options = ZCatalog.manage_options
    
    security = ClassSecurityInfo()
    
    manage_options = ZCatalog.manage_options + \
        ({'label': 'Rebuild catalog',
         'action': 'manage_rebuildCatalog',}, )

    def __init__(self, id=CONTACT_CATALOG, title='', vocab_id=None, container=None):
        """We hook up the brains now"""
        ZCatalog.__init__(self, id, title, vocab_id, container)
        #self._catalog = ReferenceBaseCatalog()

    def __url(self, ob, contact):
        return '/'.join( ob.getPhysicalPath() )+"@@contacts?id="+str(contact.id) # TODO: change this when we can get the id
        

    def catalog_object(self, obj, uid=None, idxs=None, update_metadata=1,
                       pghandler=None):
        # Wraps the object with workflow and accessibility
        # information just before cataloging.
        # XXX: this method violates the rules for tools/utilities:
        # it depends on a non-utility tool
        wftool = getToolByName(self, 'portal_workflow', None)
        if wftool is not None:
            vars = wftool.getCatalogVariablesFor(obj)
        else:
            vars = {}
        w = IndexableObjectWrapper(vars, obj)
        ZCatalog.catalog_object(self, w, uid, idxs, update_metadata,
                                pghandler)
        

    security.declarePrivate('indexObject')
    def indexObject(self, ob, contact):
        """Add to catalog.
        """
        url = self.__url(ob, contact)
        # we wrap it inside a acquisition wrapper to have access to the object later on
        self.catalog_object(contact.__of__(ob), url)

    security.declarePrivate('unindexObject')
    def unindexObject(self, ob, contact):
        """Remove from catalog.
        """
        url = self.__url(ob, contact)
        self.uncatalog_object(url)

    security.declarePrivate('reindexObject')
    def reindexObject(self, object, idxs=[], update_metadata=1, uid=None):
        """Update catalog after object data has changed.

        The optional idxs argument is a list of specific indexes
        to update (all of them by default).

        The update_metadata flag controls whether the object's
        metadata record is updated as well.

        If a non-None uid is passed, it will be used as the catalog uid
        for the object instead of its physical path.
        """
        if uid is None:
            uid = self.__url(object)
        if idxs != []:
            # Filter out invalid indexes.
            valid_indexes = self._catalog.indexes.keys()
            idxs = [i for i in idxs if i in valid_indexes]
        self.catalog_object(object, uid, idxs, update_metadata)

    security.declareProtected(SearchZCatalog, 'searchResults')     
    def searchResults(self, REQUEST=None, **kw):
        """Calls ZCatalog.searchResults with extra arguments that
        limit the results to what the user is allowed to see.

        This version uses the 'effectiveRange' DateRangeIndex.

        It also accepts a keyword argument show_inactive to disable
        effectiveRange checking entirely even for those without portal
        wide AccessInactivePortalContent permission.
        """
        kw = kw.copy()
        return ZCatalog.searchResults(self, REQUEST, **kw)

    __call__ = searchResults

    
InitializeClass(ContactCatalog)


# the utility we use
# 


class ContactIndexUtility(object):
    """a utility which uses the catalog for indexing contacts"""
    implements(IContactIndex)
    
    def indexContact(self, ob,contact):
        """add a new contact for that object"""
        catalog = getToolByName(ob,CONTACT_CATALOG, None)
        if catalog is not None:
            catalog.indexObject(ob, contact)
        
    def unindexContact(self, ob,contact):
        """remove contact for that object"""
        pass
        
    def reindexContact(self, ob,contact):
        """reindex a changed contact for that object"""
        pass
        
    def _getContact(self,root,item):
        """retrieve an item"""
        path = "/".join(item.path)            
        obj = root.unrestrictedTraverse(path)
        mgr = IContactManager(obj)
        return mgr.get_contact(item.id).__of__(obj)
        
                
    def getLatestContacts(self, ob, amount=5):
        """return the latest contacts in the subtree starting with object ob"""
        catalog = getToolByName(ob,CONTACT_CATALOG, None)
        path = "/".join(ob.getPhysicalPath())
        items = catalog.searchResults(path=path,sort_on="created", sort_order="reverse")
        root = ob.portal_url.getPortalObject()
        return [self._getContact(root,item) for item in items]
        
    
    def getContactsInModeration(self, path, start,amount=20):
        """return a list of contacts in moderation starting at path"""
        pass
        
    def getContactsMarkedAsSpam(self, path, start, amount=20):
        """return a list of contacts in spam state starting at path"""
        pass
        
    

