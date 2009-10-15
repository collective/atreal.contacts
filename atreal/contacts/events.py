"""
"""

import logging
from atreal.contacts.config import PROJECTNAME
logger = logging.getLogger(PROJECTNAME)

def indexContact(obj, event):
    """
    """
    logger.info("INDEX CONTACT " + str(event))
    if obj._p_jar is None:
        return
    if obj.getPhysicalPath()[-3] == "portal_factory":
        return
    try:
        obj.portal_contacts.catalog_object(obj)
    except KeyError, e:
        logger.error("ERROR WHILE CATALOGING CONTACT " + str(e))

def unindexContact(obj, event):
    """
    """
    obj.portal_contacts.uncatalog_object("/".join(obj.getPhysicalPath()))
