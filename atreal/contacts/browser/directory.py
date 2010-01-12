""" Define a browser view for the Contact content type. 
"""

from Products.Five.browser import BrowserView

class DirectoryView (BrowserView):
    """ Default view of a contact
    """
    
    def search_terms(self):
        """
        """
        return self.request.form.get('search_terms', '')
    
    def search_results(self):
        """
        """
        terms = self.request.form.get('search_terms', '')
        objPath = "/".join(self.context.getPhysicalPath())
        pc = self.context.portal_contacts
        if terms == "*":
            return pc(sort_on='sortable_title',
                      path={'query': objPath, 'depth':1})
        else:    
            return pc(SearchableText=terms, sort_on='sortable_title',
                      path={'query': objPath, 'depth':1})

    def itemRowClass(self, oddity):
        """
        """
        if oddity:
            return "odd"
        else:
            return "even"
