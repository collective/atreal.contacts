""" Define a browser view for the Contact content type. 
"""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from atreal.contacts.interfaces import IContact

class DirectoryView (BrowserView):
    """ Default view of a contact
    """
    
    def search_terms(self):
        return self.request.form.get('search_terms', '')
    
    
    def search_results(self):
        terms = self.request.form.get('search_terms', '')
        pc = self.context.portal_contacts
        return pc(SearchableText=terms)

    def itemRowClass(self, oddity):
        if oddity:
            return "odd"
        else:
            return "even"
