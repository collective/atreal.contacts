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
        portal_type = self.request.form.get('type', '')
        objPath = "/".join(self.context.getPhysicalPath())
        pc = self.context.portal_contacts
        query = dict(sort_on='sortable_title',
                     path={'query': objPath, 'depth': 1})
        if not terms and not portal_type:
            return []

        if terms != "*":
            query['SearchableText'] = terms

        if portal_type:
            query['portal_type'] = portal_type

        return pc(**query)

    def itemRowClass(self, oddity):
        """
        """
        if oddity:
            return "odd"
        else:
            return "even"

    def commonCounter(self, portal_type):
        """
        """
        return len(self.context.portal_contacts(portal_type=portal_type,
                      path={'query': "/".join(self.context.getPhysicalPath()),
                            'depth': 1}))

    def countContact(self):
        """
        """
        return self.commonCounter('Contact')

    def countOrganization(self):
        """
        """
        return self.commonCounter('Organization')

