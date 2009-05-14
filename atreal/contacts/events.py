

def indexContact(obj, event):
    print "INDEX CONTACT", event
    if obj._p_jar is None:
        return
    if obj.getPhysicalPath()[-3] == "portal_factory":
        return
    try:
        obj.portal_contacts.catalog_object(obj)
    except KeyError, e:
        print "ERROR WHILE CATALOGING CONTACT", e


def unindexContact(obj, event):
    obj.portal_contacts.uncatalog_object("/".join(obj.getPhysicalPath()))




