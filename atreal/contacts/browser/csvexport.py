""" Define a browser view csv export of a contact directory
"""

import csv
from StringIO import StringIO
from Products.Five.browser import BrowserView

field_list = [
    'portal_type',
    'organization',
    'civility_title',
    'firstname',
    'lastname',
    'job_title',
    'department',
    'address',
    'address_complement',
    'postcode',
    'city',
    'country',
    'email',
    'website',
    'office_phone',
    'mobile_phone',
    'private_phone',
    'fax_number',
]
md_list = [
    'subject',
]


class CsvExportView (BrowserView):
    """ Csv export view of a contact directory
    """
    
    def writeLine(self, writor, obj):
        fields = []
        for name in field_list:
            value = getattr(obj, name, '')
            if value is None:
                value = ""
            elif not isinstance(value, (str, unicode)):
                value = value.Title()
            fields.append(value)
        for name in md_list:
            value = ""
            if name in obj._md.keys(): 
                value = obj._md[name]
            if value is None:
                value = ""
            elif isinstance(value, tuple):
                value = " - ".join(value).encode('utf-8')
            elif not isinstance(value, (str, unicode)):
                value = value.Title()
            fields.append(value)
        #data += ",".join(fields)+"\n"
        writor.writerow(fields)

    def __call__(self):
        pcon = self.context.portal_contacts
        dpath = '/'.join(self.context.getPhysicalPath())
        #data = ",".join(field_list)+"\n"
        datafile = StringIO()
        writor = csv.writer(datafile)
        writor.writerow(field_list+md_list)
        
        for brain in pcon(path={'query': dpath, 'depth': 1,},
                          portal_type="Organization"):
            obj = brain.getObject()
            self.writeLine(writor, obj)

        for brain in pcon(path={'query': dpath, 'depth': 1,},
                          portal_type="Contact"):
            obj = brain.getObject()
            self.writeLine(writor, obj)

        #return data
        self.request.response.addHeader('Content-Disposition', "attachment; filename=directory_export.csv")
        self.request.response.addHeader('Content-Type', "text/csv")
        self.request.response.addHeader('Content-Length', "%d" % datafile.len)
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader('Cache-Control', "must-revalidate, post-check=0, pre-check=0, public")
        self.request.response.addHeader('Expires', "0")
        return datafile.getvalue()


mailing_field_list = [
    'civility_title',
    'firstname',
    'lastname',
    'organization',
    'address',
    'address_complement',
    'postcode',
    'city',
    'country',
    'email',
]

class CsvMailingView (BrowserView):
    """ Csv mailing view of a contact directory
    """
    def writeLine(self, writor, obj):
        fields = []
        # contact civility firstname and surname
        fields.append(getattr(obj, 'civility_title', ''))
        fields.append(getattr(obj, 'firstname', ''))
        fields.append(getattr(obj, 'lastname', ''))
        # organization
        if obj.portal_type == 'Organization':
            # organization name
            fields.append(getattr(obj, 'title', ''))
            # address
            fields.append(getattr(obj, 'address', ''))
            fields.append(getattr(obj, 'address_complement', ''))
            fields.append(getattr(obj, 'postcode', ''))
            fields.append(getattr(obj, 'city', ''))
            fields.append(getattr(obj, 'country', ''))
            # email
            fields.append(getattr(obj, 'email', ''))
        elif obj.portal_type == 'Contact':
            organization = getattr(obj, 'organization', '')
            if organization is None:
                organization = ""
            elif not isinstance(organization, (str, unicode)):
                organization = organization.Title()
            fields.append(organization)
            # address
            if not (getattr(obj, 'address', '') == '' and getattr(obj, 'address_complement', '') == '' and getattr(obj, 'postcode', '') == '' and getattr(obj, 'city', '') == '' and getattr(obj, 'country', '') == ''):
                fields.append(getattr(obj, 'address', ''))
                fields.append(getattr(obj, 'address_complement', ''))
                fields.append(getattr(obj, 'postcode', ''))
                fields.append(getattr(obj, 'city', ''))
                fields.append(getattr(obj, 'country', ''))
            else :
                # organization address
                orga = obj.getOrganization()
                fields.append(getattr(orga, 'address', ''))
                fields.append(getattr(orga, 'address_complement', ''))
                fields.append(getattr(orga, 'postcode', ''))
                fields.append(getattr(orga, 'city', ''))
                fields.append(getattr(orga, 'country', ''))
            # email
            if not (getattr(obj, 'email', '') == ''):
                fields.append(getattr(obj, 'email', ''))
            else:
                # organization email
                orga = obj.getOrganization()
                fields.append(getattr(orga, 'email', ''))
        writor.writerow(fields)


    def __call__(self):
        pcon = self.context.portal_contacts
        dpath = '/'.join(self.context.getPhysicalPath())
        datafile = StringIO()
        writor = csv.writer(datafile)
        writor.writerow(mailing_field_list)

        for brain in pcon(path={'query': dpath, 'depth': 1,},sort_on='getOrganizationUID'):
            obj = brain.getObject()
            self.writeLine(writor, obj)

        self.request.response.addHeader('Content-Disposition', "attachment; filename=directory_export.csv")
        self.request.response.addHeader('Content-Type', "text/csv")
        self.request.response.addHeader('Content-Length', "%d" % datafile.len)
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader('Cache-Control', "must-revalidate, post-check=0, pre-check=0, public")
        self.request.response.addHeader('Expires', "0")
        return datafile.getvalue()


