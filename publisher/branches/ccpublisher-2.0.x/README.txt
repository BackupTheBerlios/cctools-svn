P6 App Lifecycle
================

P6 is a framework for developing simple, "wizard"-based publishing applications.  Applications have the following features:

* Users select one or more "items" for upload.  Items can be files, CD tracks or any arbitrary chunk of data.
* Users supply metadata about their item.  Metadata is divided into sections, and each section can apply to either the entire submission or each item.  Sections which apply to each item are collected for each item individually.
* Once the user has supplied the metadata, the items along with their metadata are published to some backend.  Backends can be as simple as a local tar file, or as complex as FTP uploads with calls to confirmation web services.
* After the publishing process is complete, the user may be presented with additional opportunities to blog the item, email friends, etc.

P6 Tech Overview
================

P6 is a loosely coupled framework that aims to provide common, generic services to applications and push application-specific functionality down to the client application.

P6 provides the following packages:

* p6.ui
    Window and application classes, interfaces pages should adhere to.

* p6.metadata
    Metadata interfaces, basic class definitions, metadata events.

* p6.storage
    Interfaces for backend storage providers, sample implementation.

An application wishing to use the P6 framework would:

1) Create a primary frame class; this is mostly just a dead chicken and it'd be good to get rid of it if possible
2) Provide a list of page classes.  Some standard pages (file selector, etc) are provided in the p6.ui.pages package, but any wx.Panel subclass may be used so long as it conforms to the specified interface.  
3) Define your metadata fields, or use the stock collection.  
4) Listen for events.  P6 publishes events for item selection, metadata field changes, and backend interaction.  If you're implementing your own backend, for example, you'll need to listen for StoreItem events.

