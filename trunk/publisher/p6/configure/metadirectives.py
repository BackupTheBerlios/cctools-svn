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

    choices = zope.configuration.fields.Tokens(
        title=u"",
        description=u"",
        required=False,
        value_type=zope.configuration.fields.MessageID(),
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

