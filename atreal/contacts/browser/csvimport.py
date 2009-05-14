""" Define a browser view csv import of a contact directory
"""

import csv

from Products.Five.browser import BrowserView

from atreal.contacts import ContactsMessageFactory as _


class CsvImportView (BrowserView):
    """ Csv import view of a contact directory
    """
    
    def __call__(self):
        pcon = self.context.portal_contacts
        
        method = self.request.get('REQUEST_METHOD', 'GET')
        if (method != 'POST') or not int(self.request.form.get('form.submitted', 0)):
            return self.index()
        
        if self.request.form.get('form.button.Cancel', "") != 'Cancel':
            pt = self.context.portal_types
            
            if bool(int(self.request.form.get('delete_existing', 0))):
                self.context.manage_delObjects(self.context.objectIds())
                self.context.reindexObject()
            
            file_upload = self.request.form.get('csv_upload', None)
            if file_upload is None:
                pass
            reader = csv.reader(file_upload)
            header = reader.next()[1:]
            for line in reader:
                type, line = line[0], line[1:]
                entry_id = self.context.generateUniqueId(type)
                pt.constructContent(type, self.context, entry_id)
                entry = self.context[entry_id]
                
                for name, value in zip(header, line):
                    print "Setting %s = %s" % (name, value)
                    field = entry.getField(name)
                    if field is None:
                        continue
                    if (type == 'Contact') and (name == 'organization'):
                        if value:
                            orgas = pcon(portal_type="Organization",
                                        Title=value)
                            if len(orgas)>0:
                                value = orgas[0].getObject()
                            else:
                                value = None
                        else:
                            value = None
                            
                    field.set(entry, value)
                entry.reindexObject()
                pcon.catalog_object(entry)
        
        self.context.reindexObject()    
        

        message = _(u'The CSV file has been imported.',
                    mapping={u'title' : self.context.Title()})
        self.context.plone_utils.addPortalMessage(message)
        
        self.request.response.redirect(self.context.absolute_url())
        
    
