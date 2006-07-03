# p6.storage.tests.testStorageRegistry
#
# Unittests for the P6 storage provider registry
#

import p6.storage.registry

class dummyProvider(object):
    """Dummy storage provider used for testing."""
    
class dummyProvider2(object):
    """Dummy storage provider used for testing."""

    
def testRegistryInitialization():
    """Registry initializes empty."""

    registry = p6.storage.registry.StorageRegistry()

    assert registry.identifiers() == []

def testRegistration():
    """Objects may be registered and retrieved properly."""

    registry = p6.storage.registry.StorageRegistry()

    # register an object
    registry.register('id', 'provider', dummyProvider)

    # make sure it was registered with the correct ID.
    assert registry.identifiers() == ['id']
    assert isinstance(registry['id'], p6.storage.registry.StorageRegistryItem)

    # make sure the correct information was stored in the registry item
    assert registry['id'].name == 'provider'
    assert registry['id'].description == ''

def testSequencing():
    """Object identifiers should be returned in registered order."""

    registry = p6.storage.registry.StorageRegistry()

    # register two objects
    registry.register('id', 'provider', dummyProvider, 'description')
    registry.register('id2', 'provider', dummyProvider2)

    # make sure the order was retained
    assert registry.identifiers() == ['id', 'id2']
    
def testLookup():
    """Objects may be registered, and then looked up by identifier."""

    registry = p6.storage.registry.StorageRegistry()

    # register two objects
    registry.register('id', 'provider', dummyProvider)
    registry.register('id2', 'provider2', dummyProvider2, 'description')
    
    assert len(registry.identifiers()) == 2
    assert isinstance(registry['id'], p6.storage.registry.StorageRegistryItem)
    assert isinstance(registry['id2'], p6.storage.registry.StorageRegistryItem)
    
