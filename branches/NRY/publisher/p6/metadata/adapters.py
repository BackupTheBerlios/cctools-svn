import zope.interface
import zope.component

import p6
import interfaces

#@zope.interface.implementer(interfaces.IXmlString)
#@zope.component.adapter(interfaces.IMetadataGroup)
def groupToXml(metaGroup):
    if metaGroup.appliesTo is not None:
        # != p6.storage.interfaces.IWork:
        elements = "\n".join(["<%s>%s</%s>" % (n.id, n(), n.id) for n in
                   metaGroup.getFields()])
        return "<%s>\n%s\n</%s>" % (metaGroup.id, elements, metaGroup.id)
    else:
        return None

#zope.component.provideAdapter(groupToXml)
