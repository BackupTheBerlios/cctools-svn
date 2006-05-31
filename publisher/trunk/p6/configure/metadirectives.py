"""Component architecture related 'zope' ZCML namespace directive interfaces

$Id$
"""
__docformat__ = 'restructuredtext'

import zope.configuration.fields
import zope.interface
import zope.schema

_ = unicode

class IStorageDirective(zope.interface.Interface):
    """Storage instantiation."""
    name = zope.configuration.fields.MessageID(
        title=u"Name.",
        description=u"",
        required=True,
        )

    factory = zope.configuration.fields.GlobalObject(
        title=u"Storage Factory callable",
        description=u"",
        required=True,
        )
    
class IMdataGroupDirective(zope.interface.Interface):
    """Metadata grouping."""

    id = zope.configuration.fields.MessageID(
        title=u"Unique identifier",
        description=u"",
        required=True,
        )

    title= zope.configuration.fields.MessageID(
        title=u"Unique identifier",
        description=u"",
        required=True,
        )

    description= zope.configuration.fields.MessageID(
        title=u"Group description",
        description=u"",
        required=False,
        )
    
    for_ = zope.configuration.fields.GlobalInterface(
        title=u"",
        description=u"",
        required=True,
        )

    factory = zope.configuration.fields.GlobalObject(
        title=u"",
        description=u"",
        required=False,
        )

    persistMode = zope.configuration.fields.PythonIdentifier(
        title=u"Persistence Mode",
        description=u"Hint to the framework on how to handle fields "
                     "which register as available for persistence. "
                     "Valid values are 'always', 'never', or 'prompt'. ",
        required=False,
        )

class IMetadataFieldSubdirective(zope.interface.Interface):
    """  """

    id = zope.configuration.fields.MessageID(
        title=u"",
        description=u"",
        required=True,
        )

    type = zope.configuration.fields.GlobalInterface(
        title=u"",
        description=u"",
        required=True,
        )

    label = zope.configuration.fields.MessageID(
        title=u"",
        description=u"",
        required=False,
        )

    description = zope.configuration.fields.MessageID(
        title=u"",
        description=u"",
        required=False,
        )

    tip = zope.configuration.fields.MessageID(
        title=u"",
        description=u"",
        required=False,
        )

    choices = zope.configuration.fields.Tokens(
        title=u"",
        description=u"",
        required=False,
        value_type=zope.configuration.fields.MessageID(),
        )

    choicesList = zope.configuration.fields.GlobalObject(
        title=u"Choices List",
        description=u"A Python sequence which provides the selection choices",
        required=False,
        )

    validator = zope.configuration.fields.GlobalObject(
        title=u"validator",
        description=u"A callable which returns None if the passed value "
                     "validates, or a String if there is an error.",
        required=False,
        )

    persist = zope.configuration.fields.Bool(
        title=u"persist",
        description=u"If true, the user-supplied value will be made "
                     "available for persistence.",
        required=False,
        )

    canonical = zope.configuration.fields.MessageID(
        title=u"canonical",
        description=u"The canonical URI for this field.",
        required=False,
        )
        
    
class IPagesDirective(zope.interface.Interface):
    """Assembly of pages which defines a wizard-like application."""

    appid = zope.configuration.fields.Tokens(
        title=u"The application ID.",
        required=True,
        value_type=zope.configuration.fields.PythonIdentifier(),
        )

class IPageSubdirective(zope.interface.Interface):
    """A single page."""

    title= zope.configuration.fields.MessageID(
        title=u"Unique identifier",
        description=u"",
        required=False,
        )

    factory = zope.configuration.fields.GlobalObject (
        title=u"The page factory.",
        description=u"The page factory; the factory should take a single "
               "argument,"
               " the parent window, and return an object conforming to "
               "IWizardPage.",
        required=True,

        )

class IMetadataPagesSubdirective(zope.interface.Interface):
    """A sequence of pages generated from the metadata."""

    for_ = zope.configuration.fields.Tokens(
        title=_("Interfaces"),
        description=_("The interfaces which metadata applies to."),
        required=False,
        value_type=zope.configuration.fields.GlobalInterface(),
        )

class IFileSelectorSubdirective(zope.interface.Interface):
    """File selector page."""
    
class IStorePageSubdirective(zope.interface.Interface):
    """A generic storage page which is able to emit and handle the
    appropriate events."""

class IStorageSelector(zope.interface.Interface):
    """A page which allows users to select one or more storage providers
    to upload to."""

    multi = zope.configuration.fields.Bool(
        title = _("Multiple"),
        description = _("Allow multiple storage providers to be selected."),
        required=False,
        )

class IExtensionPoint(zope.interface.Interface):
    """ XXX """

    for_ = zope.configuration.fields.GlobalInterface(
        title=u"",
        description=u"",
        required=True,
        )

class IFinalUrlPage(zope.interface.Interface):
    """ XXX """

    title = zope.configuration.fields.MessageID(
        title=u"The page title.",
        required=True,
        )
    
class IXmldisplayPageSubdirective(zope.interface.Interface):
    """A generic page which displays a psuedo-XML representation of the
    metadata collected."""
    
class IXrcPageSubdirective(zope.interface.Interface):
    """A customizable XRC page."""

    title = zope.configuration.fields.MessageID(
        title=u"The page title.",
        required=True,
        )

    xrcfile = zope.configuration.fields.Path(
        title=u"XRC filename",
        description=u"",
        required=True,
        )
    
    xrcid = zope.configuration.fields.MessageID(
        title=u"XRC Id",
        description=u"",
        required=True,
        )
    
class IPreferencesDirective(zope.interface.Interface):
    """A container for an extension preference set."""

    id = zope.configuration.fields.MessageID(
        title=u"A unique ID for this extension/preference set.",
        required=True,
        )

    label = zope.configuration.fields.MessageID(
        title=u"Title used for the preferences page.",
        required=True,
        )

class IPrefsFieldSubdirective(zope.interface.Interface):
    """A single preference field."""

    id = zope.configuration.fields.MessageID(
        title=u"The unique identifier for this field.",
        required=True,
        )

    type = zope.configuration.fields.GlobalObject(
        title=u"Global factory class for this field (str, dict, etc).",
        required=True,
        )

    label = zope.configuration.fields.MessageID(
        title=u"Label to use in preferences UI.",
        required=False,
        )
    
class IExtensionDirective(zope.interface.Interface):
    """An extension registration."""

    id = zope.configuration.fields.MessageID(
        title=u"",
        required=True,
        )

    name = zope.configuration.fields.MessageID(
        title=u"",
        required=True,
        )

    description = zope.configuration.fields.MessageID(
        title=u"",
        required=False,
        )
    
    locale = zope.configuration.fields.Path(
        title=u"Relative path containing locale files.",
        required=False,
        )
