"""
"""

from zope.interface import Interface
from zope.app.container.constraints import contains
from zope import schema

from atreal.contacts import ContactsMessageFactory as _

class IContactsLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """

class IDirectory (Interface):
    """ A folder containing contacts
    """
    contains ('atreal.contacts.interfaces.IContact',
              'atreal.contacts.interfaces.IOrganization')    
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    description = schema.TextLine(title=_(u"Description"),
                                  description=_(u"A short summary of this folder"))

class IGenericContact(Interface):
    """ An element representing a contact or an organization
    """
    
class IContact (IGenericContact):
    """ An element representing a contact
    """
    
class IOrganization (IGenericContact):
    """ An element representing an organization
    """

class IContactCatalog(Interface):
    """ Marker interface for contact catalog
    """

class IContactIndex(Interface):
    """ Interface for indexing and retrieving contacts
    """

    def indexContact(object, contact):
        """ Add a new contact for that object
        """

    def unindexContact(object, contact):
        """ Remove contact for that object
        """

    def reindexContact(object, contact):
        """ Reindex a changed contact for that object
        """

    def getLatestContacts(path, amount=5):
        """ Return the latest contacts in the subtree starting with path
        """

    def getContactsInModeration(path, start, amount=20):
        """ Return a list of contacts in moderation starting at path
        """

    def getContactsMarkedAsSpam(path, start, amount=20):
        """ Return a list of contacts in spam state starting at path
        """
