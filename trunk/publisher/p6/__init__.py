"""
P6
==
@author: Nathan R. Yergler <nathan@creativecommons.org>
@organization: Creative Commons
@copyright: copyright 2005, Creative Commons, Nathan R. Yergler
@license: Licensed under the GNU GPL 2

P6 is a loosely coupled framework that aims to provide common, generic services to applications and push application-specific functionality down to the client application.

P6 provides the following packages:

* p6.ui
    Window and application classes, interfaces pages should adhere to.

* p6.metadata
    Metadata interfaces, basic class definitions, metadata events.

* p6.storage
    Interfaces for backend storage providers, sample implementation.

P6 is a framework for developing simple, "wizard"-based publishing applications.  Applications have the following features:

* Users select one or more "items" for upload.  Items can be files, CD tracks or any arbitrary chunk of data.
* Users supply metadata about their item.  Metadata is divided into sections, and each section can apply to either the entire submission or each item.  Sections which apply to each item are collected for each item individually.
* Once the user has supplied the metadata, the items along with their metadata are published to some backend.  Backends can be as simple as a local tar file, or as complex as FTP uploads with calls to confirmation web services.
* After the publishing process is complete, the user may be presented with additional opportunities to blog the item, email friends, etc.
"""

import wx

import zope.interface

import metadata
import ui
import storage
import configure
import app

