import zope.interface
import zope.component

import p6
import interfaces

def groupToXml(metaGroup):
    if metaGroup.appliesTo is not None:
        # != p6.storage.interfaces.IWork:
        elements = "\n".join(["<%s>%s</%s>" % (n.id, n(), n.id) for n in
                   metaGroup.getFields()])
        return "<%s>\n%s\n</%s>" % (metaGroup.id, elements, metaGroup.id)
    else:
        return None

def itemMetadata(mGroup, item):
    result = {}
    
    if mGroup.appliesTo not in zope.interface.implementedBy(item.__class__):
        return None
    else:
        for field in mGroup.getFields():
            f_key = field.id or field.key
            f_value = field()

            if isinstance(f_value, dict):
                if item.getIdentifier() in f_value:
                    f_value = f_value[item.getIdentifier()]
                else:
                    f_value = f_value[p6.metadata.base.DEFAULT_KEY]

            result[f_key] = f_value

    return result
