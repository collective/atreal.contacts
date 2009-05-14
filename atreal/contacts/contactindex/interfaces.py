from zope.interface import Interface

class IContactCatalog(Interface):
    """Marker interface for comment catalog
    """

class IIndexableObjectWrapper(Interface):

    """ Wrapper for catalogued objects, for indexing "virtual" attributes.
    """

