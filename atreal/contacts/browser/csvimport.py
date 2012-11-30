""" Define a browser view csv import of a contact directory
"""

import csv

from Products.Five.browser import BrowserView
from plone.i18n.normalizer.interfaces import IUserPreferredURLNormalizer

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
            objPath = "/".join(self.context.getPhysicalPath())
            
            import_mode = int(self.request.form.get('delete_existing', 0))

            if import_mode == 2:
                self.context.manage_delObjects(self.context.objectIds())
                self.context.reindexObject()
            
            file_upload = self.request.form.get('csv_upload', None)
            if file_upload is None:
                pass

            reader = csv.reader(file_upload)
            firstline = reader.next()
            has_id_column = firstline[0] == 'id'
            if has_id_column:
                header = firstline[2:]
            else:
                header = firstline[1:]
            
            normalizer = IUserPreferredURLNormalizer(self.request)

            for line in reader:
                if has_id_column:
                    entry_id, line = line[0], line[1:]

                type, infos = line[0], line[1:]
                organization, civility, firstname, lastname = infos[0:4]
                if type == 'Organization':
                    title = organization
                elif type == 'Contact':
                    title = "%s %s" % (firstname, lastname)
                else:
                    raise ValueError, "Entry must have a type : %s" % line
                
                if not has_id_column:
                    entry_id = normalizer.normalize(title)

                if import_mode == 1 and entry_id in self.context:
                    #Delete contents that exists
                    self.context.manage_delObjects([entry_id])
                    
                if not(import_mode == 0 and entry_id in self.context):
                    #Do not create contents that ever exist
                    pt.constructContent(type, self.context, entry_id)

                entry = self.context[entry_id]
                     
                for name, value in zip(header, infos):
                    print "Setting %s = %s" % (name, value)
                    if (name == 'organization') and (type == 'Organization'):
                        name = 'title'
                    field = entry.getField(name)
                    if field is None:
                        continue
                    if (type == 'Contact') and (name == 'organization'):
                        if value:
                            orgas = pcon(portal_type="Organization",
                                         path={'query': objPath, 'depth':1},
                                         Title=value)
                            if len(orgas)>0:
                                value = orgas[0].getObject()
                            else:
                                orga_id = self.context.generateUniqueId('Organization')
                                pt.constructContent('Organization', self.context, orga_id, title=value)
                                orga = self.context[orga_id]
                                orga.processForm()
                                pcon.catalog_object(orga)
                                value = orga
                        else:
                            value = None

                    if not value and import_mode == 0:
                        # do not set empty values if "keep all contacts" option is selected
                        continue
                    else: 
                        field.set(entry, value)

                entry.processForm()
                pcon.catalog_object(entry)
        
        self.context.reindexObject()    
        

        message = _(u'The CSV file has been imported.',
                    mapping={u'title' : self.context.Title()})
        self.context.plone_utils.addPortalMessage(message)
        
        self.request.response.redirect(self.context.absolute_url())
        
    
