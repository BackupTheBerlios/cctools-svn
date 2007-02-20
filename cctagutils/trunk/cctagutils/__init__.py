# cctagutils Python package
__id__ = "$Id:"

# bring package modules into the root namespace
import rdf
import const
import lookup
import metadata

# define constants to use for verification status
VERIFY_VERIFIED = 1
VERIFY_NO_RDF = 0
VERIFY_NO_WORK = -1
VERIFY_NO_MATCH = -2
VERIFY_NO_CLAIM = -3
VERIFY_CONFLICTING_ASSERTIONS = -4
