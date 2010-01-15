""" Define a browser view for the Contact content type. 
"""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone import PloneMessageFactory as _

from atreal.contacts.interfaces import IContact

class OrganizationView(BrowserView):
    """ Default view of a contact
    """
    
    def getEmployees(self):
        pc = getToolByName(self.context, 'portal_contacts')
        brains = pc(portal_type="Contact",
                   getOrganizationUID=self.context.UID(),
                   sort_on='sortable_title')
        return brains
    
    def employRowClass(self, oddity):
        if oddity:
            return "odd"
        else:
            return "even"

    def showAddress(self):
        for name in ('address', 'address_complement', 'postcode',
                     'city', 'country'):
            value = self.context.schema[name].get(self.context)
            if value:
                return True
        return False


class OrganizationDelConfirm(BrowserView):
    """ Deletion confirmation
    """
    
    def __call__(self):
        method = self.request.get('REQUEST_METHOD', 'GET')
        if (method != 'POST') or not int(self.request.form.get('form.submitted', 0)):
            return self.index()
        
        if self.request.form.get('form.button.Cancel') == 'Cancel':
            #User canceled deletion...
            message = _(u'The deletion of ${title} has been canceled.',
                        mapping={u'title' : self.context.Title()})
            self.context.plone_utils.addPortalMessage(message)
            self.request.response.redirect(self.context.absolute_url())
            return
        
        parent = self.context.aq_inner.aq_parent
        
        self.processChilds()
        
        parent.manage_delObjects(self.context.getId())
        
        title = self.context.Title()
        message = _(u'${title} has been deleted.',
                    mapping={u'title': self.context.Title()})
        transaction_note('Deleted %s' % self.context.absolute_url())
        self.context.plone_utils.addPortalMessage(message)
        
        self.request.response.redirect(parent.absolute_url())
    
    def processChilds(self):
        childs = self.getEmployees()
        if not childs:
            return
        parent = self.context.aq_inner.aq_parent
        cascade = self.request.form.get('cascade', "clear_link")
        if cascade == "delete":
            message = _(u"Deleted all contacts linked to the '${title}' organisation",
                        mapping={u'title' : self.context.Title()})
            for child in childs:
                parent.manage_delObjects([child.getId])
        else:
            message = _(u"Unlinked all the contacts from the '${title}' organisation",
                        mapping={u'title' : self.context.Title()})
            for child in childs:
                child_obj = child.getObject()
                child_obj.setOrganization("")
                child_obj.reindexObject()
                parent.portal_contacts.catalog_object(child_obj)
        self.context.plone_utils.addPortalMessage(message)
    
    def getEmployees(self):
        pc = getToolByName(self.context, 'portal_contacts')
        brains = pc(portal_type="Contact",
                   getOrganizationUID=self.context.UID(),
                   sort_on='sortable_title')
        print "getEmployees yielded %d contacts" % len(brains)
        return brains
