""" Definition of the Contact content type.
"""

import transaction

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from atreal.contacts.interfaces import IContact
from atreal.contacts.config import PROJECTNAME

from atreal.contacts import ContactsMessageFactory as _

ContactSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    #
    atapi.StringField('firstname',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_firstname',
                    default=u"First Name"),
            description=_(u'help_firstname',
                          default=u""))
        ),

    atapi.StringField('lastname',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_lastname',
                    default=u"Last Name"),
            description=_(u'help_lastname',
                          default=u""))
        ),
    
    atapi.StringField('job_title',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_job_title',
                    default=u"Job Title"),
            description=_(u'help_job_title',
                          default=u""))
        ),
    
    #
    atapi.ReferenceField('organization',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory='atreal.contacts.vocabularies.organizations',
        relationship='isEmployeeOf',
        widget=atapi.ReferenceWidget(
            label=_(u'label_organization',
                    default=u"Organization"),
            description=_(u'help_organization',
                          default=u""))
        ),

    atapi.StringField('department',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_department',
                    default=u"Department"),
            description=_(u'help_department',
                          default=u""))
        ),
    
    #  
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
    
    atapi.StringField('mobile_phone',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_mobile_phone',
                    default=u"Mobile Phone"),
            description=_(u'help_mobile_phone',
                          default=u""))
        ),
    
    atapi.StringField('private_phone',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'label_private_phone',
                    default=u"Private Phone"),
            description=_(u'help_private_phone',
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

ContactSchema['title'].mode = 'r'
ContactSchema['title'].storage = atapi.AnnotationStorage()
ContactSchema['title'].required = False

ContactSchema['description'].storage = atapi.AnnotationStorage()
ContactSchema['description'].mode = 'r'
ContactSchema['description'].widget.label = _(u'label_description', default=u"Description")
ContactSchema['description'].widget.description = _(u'help_description', default=u"")

finalizeATCTSchema (ContactSchema, folderish=False, moveDiscussion=False)

class Contact (base.ATCTContent):
    """ Describe a contact.
    """
    implements(IContact)
    
    portal_type = "Contact"
    _at_rename_after_creation = True
    schema = ContactSchema
    
    title = atapi.ATFieldProperty('title')
    firstname = atapi.ATFieldProperty('firstname')
    lastname = atapi.ATFieldProperty('lastname')
    job_title = atapi.ATFieldProperty('job_title')
    organization = atapi.ATReferenceFieldProperty('organization')
    department = atapi.ATFieldProperty('department')
    address = atapi.ATFieldProperty('address')
    address_complement = atapi.ATFieldProperty('address_complement')
    postcode = atapi.ATFieldProperty('postcode')
    city = atapi.ATFieldProperty('city')
    country = atapi.ATFieldProperty('country')
    email = atapi.ATFieldProperty('email')
    website = atapi.ATFieldProperty('website')
    office_phone = atapi.ATFieldProperty('office_phone')
    mobile_phone = atapi.ATFieldProperty('mobile_phone')
    private_phone = atapi.ATFieldProperty('private_phone')
    fax_number = atapi.ATFieldProperty('fax_number')
    description = atapi.ATFieldProperty('description')
    
    def generateNewId(self):
        return self.UID()

    def Title (self):
        title = ('%s %s' % (self.getFirstname(), self.getLastname(),)).strip()
        if title :
            return title
        else :
            return "---"
    
    def setTitle(self, title):
        """
        Don't ever touch this method!!!
        It's existence prevent the parent's method to be called!
        """
        pass

    def Description (self):
        return ' '.join([' / '.join([self.getOffice_phone(), self.getEmail()])])

    def getOrganizationUID (self):
        return self.getOrganization().UID()
    
    def SearchableText(self):
        collec = []
        for name in ('firstname', 'lastname', 'job_title', 'organization',
                     'department', 'address', 'address_complement', 'city',
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



atapi.registerType (Contact, PROJECTNAME)



