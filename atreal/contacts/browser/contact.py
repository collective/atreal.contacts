""" Define a browser view for the Contact content type. 
"""

from Products.Five.browser import BrowserView

class ContactView (BrowserView):
    """ Default view of a contact
    """
    
    
    def showAddress(self):
        for name in ('address', 'address_complement', 'postcode',
                     'city', 'country'):
            value = self.context.schema[name].get(self.context)
            if value:
                return True
        return False
