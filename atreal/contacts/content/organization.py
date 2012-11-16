""" Definition of the Organization content type.
"""

import transaction

from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from atreal.contacts.interfaces import IOrganization
from atreal.contacts.interfaces import IContact
from atreal.contacts.config import PROJECTNAME

from atreal.contacts import ContactsMessageFactory as _

OrganizationSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField('address',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_address',
                    default=u"Address"),
            description=_(u'help_address',
                          default=u""))
        ),
    
    atapi.StringField('address_complement',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_address_complement',
                    default=u"Address Complement"),
            description=_(u'help_address_complement',
                          default=u""))
        ),
    
    atapi.StringField('postcode',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_postcode',
                    default=u"Post Code"),
            description=_(u'help_postcode',
                          default=u""))
        ),
    
    atapi.StringField('city',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_city',
                    default=u"City"),
            description=_(u'help_city',
                          default=u""))
        ),

    atapi.StringField('country',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_country',
                    default=u"Country"),
            description=_(u'help_country',
                          default=u""))
        ),
    #
    atapi.StringField('email',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_email',
                    default=u"Email"),
            description=_(u'help_email',
                          default=u""))
        ),
    
    atapi.StringField('website',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_website',
                    default=u"Website"),
            description=_(u'help_website',
                          default=u""))
        ),
    
    atapi.StringField('office_phone',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_office_phone',
                    default=u"Office Phone"),
            description=_(u'help_office_phone',
                          default=u""))
        ),
    
    atapi.StringField('fax_number',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_fax_number',
                    default=u"Fax Number"),
            description=_(u'help_fax_number',
                          default=u""))
        ),
    ))

OrganizationSchema['title'].storage = atapi.AnnotationStorage()
OrganizationSchema['title'].widget.label = _(u'label_organization', default=u"Organization")
OrganizationSchema['title'].widget.description = _(u'help_organization', default=u"")

OrganizationSchema['description'].storage = atapi.AnnotationStorage()
OrganizationSchema['description'].mode = 'r'
OrganizationSchema['description'].widget.label = _(u'label_description', default=u"Description")
OrganizationSchema['description'].widget.description = _(u'help_description', default=u"")

finalizeATCTSchema (OrganizationSchema, folderish=False, moveDiscussion=False)

class Organization (base.ATCTContent):
    """ Describe an organization.
    """
    implements(IOrganization)
    
    portal_type = "Organization"
    _at_rename_after_creation = True
    schema = OrganizationSchema
    
    title = atapi.ATFieldProperty('title')
    organization = atapi.ATFieldProperty('title')
    address = atapi.ATFieldProperty('address')
    address_complement = atapi.ATFieldProperty('address_complement')
    postcode = atapi.ATFieldProperty('postcode')
    city = atapi.ATFieldProperty('city')
    country = atapi.ATFieldProperty('country')
    email = atapi.ATFieldProperty('email')
    website = atapi.ATFieldProperty('website')
    office_phone = atapi.ATFieldProperty('office_phone')
    fax_number = atapi.ATFieldProperty('fax_number')

    #def generateNewId(self):
    #    return self.id
   
    def isDeletable (self):
        pc = getToolByName(self, 'portal_catalog')
        brains = pc(portal_type="Contact",
                    getOrganizationUID=self.UID())
        if len(brains) > 0:
            return False
        else:
            return True
    
    def SearchableText(self):
        collec = []
        for name in ('title', 'address', 'address_complement', 'city',
                     'country', 'email', 'website'):
            text = self.schema[name].get(self)
            if not isinstance(text, str):
                text = getattr(text, 'title', str(text))
            collec.append(text)
        return " ".join(collec)

    def sortable_title(self):
        return self.Title().lower()
    
    def directoryUID(self):
        return self.aq_inner.aq_parent.UID()

    def getOrganizationUID (self):
        return self.UID()


    def setDescription(self, description):
        """
        Don't ever touch this method!!!
        It's existence prevent the parent's method to be called!
        """
        pass

atapi.registerType (Organization, PROJECTNAME)
