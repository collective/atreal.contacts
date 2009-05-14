""" Definition of the Directory content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from atreal.contacts.interfaces import IDirectory
from atreal.contacts.config import PROJECTNAME

from atreal.contacts import ContactsMessageFactory as _

DirectorySchema = folder.ATFolderSchema.copy ()

DirectorySchema['title'].storage = atapi.AnnotationStorage ()
DirectorySchema['description'].storage = atapi.AnnotationStorage ()

finalizeATCTSchema (DirectorySchema, folderish=True, moveDiscussion=False)

class Directory (folder.ATFolder):
    """ Contains multiple contacts.
    """
    implements(IDirectory)
    
    portal_type = "Directory"
    _at_rename_after_creation = True
    schema = DirectorySchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    

atapi.registerType(Directory, PROJECTNAME)
