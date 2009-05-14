from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName

from atreal.contacts.interfaces import IOrganization

class OrganizationsVocabulary(object):
    """Vocabulary factory for organizations.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        default = [('Aucune', '')]
        items = [(r.Title, r.UID) for r in 
                    catalog(object_provides=IOrganization.__identifier__,
                            rpath=dict(query='/'.join(context.getParentNode().getPhysicalPath()),
                                       depth=1),
                            sort_on='sortable_title')]
        return SimpleVocabulary.fromItems(default + items)

OrganizationsVocabularyFactory = OrganizationsVocabulary()
