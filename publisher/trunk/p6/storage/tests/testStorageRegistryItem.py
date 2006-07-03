# p6.storage.tests.testStorageRegistry
#
# Unittests for the P6 storage provider registry item
#

import p6.storage.registry

class DummyProvider(object):
    """Placeholder class to pass in as a provider factory."""
    
def testRegistryItem():
    """RegistryItem stores information in the correct attributes."""
    
    item = p6.storage.registry.StorageRegistryItem('id', 'name', DummyProvider,
                                            'description')

    assert item.id == 'id'
    assert item.name == 'name'
    assert item.description == 'description'

def testActivation():
    """RegistryItem creates an instance of the provider when activated."""
    
    item = p6.storage.registry.StorageRegistryItem('id', 'name', DummyProvider,
                                            'description')

    # make sure activation happens properly
    item.activate()
    assert item.instance is not None
    assert isinstance(item.instance, DummyProvider)

    # repeated activations should have no effect
    a = item.instance
    item.activate()

    assert item.instance is a
    
def testDeactivation():
    """RegistryItem deletes the instance when provider is deactivated."""

    item = p6.storage.registry.StorageRegistryItem('id', 'name', DummyProvider,
                                            'description')

    # make sure deactivation happens properly
    item.activate()
    assert item.instance is not None

    item.deactivate()
    assert item.instance is None

    # deactivation before activation should have no effect
    item = p6.storage.registry.StorageRegistryItem('id', 'name', DummyProvider,
                                            'description')

    item.deactivate()
    assert item.instance is None

def testIsActivated():
    """RegistryItem reports activation status properly."""

    item = p6.storage.registry.StorageRegistryItem('id', 'name',
                                                   DummyProvider,
                                                   'description')

    assert item.isActivated() == False

    item.activate()

    assert item.isActivated() == True

    item.deactivate()

    assert item.isActivated() == False
    
