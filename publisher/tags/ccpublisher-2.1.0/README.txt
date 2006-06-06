-----------
ccPublisher
-----------

:Author: Nathan R. Yergler
:Updated: $Date$

ccPublisher is a tool for generating license information for a work and
optionally uploading it to the Internet Archive or other repository for
hosting.  

What's New
==========

For information on changes in this release, see the appropriate release
page.  Release pages may be found at 
http://wiki.creativecommons.org/CcPublisher_2_Releases.

Running ccPublisher
===================

To run ccPublisher from source, you must have the following prerequisites
installed:

* Python 2.4 or later
* wxPython 2.6 or later
* elementtree for Python

See XXX for dependency download links.

Once you have the dependencies installed, you can run ccPublisher using the
included script::

  $ ./ccPublisher.sh

The wrapper script fixes up the Python path to ensure that the default
String encoding is properly set.  

Contact Information
===================

Bugs may be reported to software@creativecommons.org (good) or recorded
in the bug tracker at http://roundup.creativecommons.org/ccpublisher
(better).  For general discussion, the #cc channel on irc.freenode.net.
The cc-devel mailing list may also be used for communication with the
developers; see http://wiki.creativecommons.org/Mailing_Lists for details.

License Information
===================

ccPublisher is licensed under the GNU GPL version 2. License information 
can be found in the file LICENSE.txt, included in this distribution.
