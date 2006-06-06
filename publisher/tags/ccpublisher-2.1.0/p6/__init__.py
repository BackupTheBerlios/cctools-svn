"""
    P6
    ==
      P6 is a loosely coupled framework for developing simple,
      "wizard"-based publishing applications.  Applications have the
      following features:
       - Users select one or more "items" for upload.  Items can be files, CD tracks or any arbitrary chunk of data.
       - Users supply metadata about their item.  Metadata is divided into sections, and each section can apply to either the entire submission or each item.  Sections which apply to each item are collected for each item individually.
       - Once the user has supplied the metadata, the items along with their metadata are published to some backend.  Backends can be as simple as a local tar file, or as complex as FTP uploads with calls to confirmation web services.
       - After the publishing process is complete, the user may be presented with additional opportunities to blog the item, email friends, etc.

      P6 provides the following packages:
       - B{p6.ui}
       
         Window and application classes, interfaces pages should adhere to.
       - B{p6.metadata}
       
         Metadata interfaces, basic class definitions, metadata events.
       - B{p6.storage}
       
         Interfaces for backend storage providers, sample implementation.

"""

import wx

import zope.interface

import metadata
import ui
import storage
import configure
import app
import i18n

VERSION = 2.0
