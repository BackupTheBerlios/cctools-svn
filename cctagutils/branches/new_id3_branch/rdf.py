"""Support functions for generation of verification RDF for embedded
license claims."""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

import re
import urllib
import os
import cctagutils.base32 as base32
import sha
from cctagutils.metadata import metadata

def getLicense(license_url):
	"""Extract license RDF from a given url; if an error occurs
	in retrieving the url, return None.
	"""
	
	lre = re.compile("<License.*?</License>", re.DOTALL)
	try:
		license_doc = urllib.urlopen(license_url).read()
		return lre.findall(license_doc)[0]
	except:
		return None
	

def fileHash(filename):
	block_size = 8192

	sha_hash = sha.new()
	in_file = file(filename, 'rb')

	block = in_file.read(block_size)

	while block:
		sha_hash.update(block)

		block = in_file.read(block_size)

	return base32.b2a(sha_hash.digest()).upper()

def generate(files, claim_url, license, year, holder,
	     source=None, license_rdf=None, work_meta={} ):

	if not(license_rdf):
		# attempt to retrieve the rdf
		license_rdf = getLicense(license)

	out = ''
	out +=  "<!-- Publish this file at " + claim_url + " -->\n"
	out += """<rdf:RDF xmlns="http://web.resource.org/cc/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n"""
	
	for f in files:
                h = fileHash(f)

		out += '<Work rdf:about="urn:sha1:'+h+'">\n'

		# get title from supplied metadata, or fall back to extraction
		if 'title' in work_meta:
			out += '\t<dc:title>'+ \
			       work_meta['title'] + '</dc:title>\n'
			
		out += '\t<dc:date>' + year + '</dc:date>\n'

		if 'description' in work_meta:
			out += '\t<dc:description>'+ \
			       work_meta['description'] +\
			       '</dc:description>\n'

		if 'creator' in work_meta:
			out += '\t<dc:creator><Agent><dc:title>'+ \
			       work_meta['creator'] +\
			       '</dc:title></Agent></dc:creator>\n'
			
		out += '\t<dc:rights><Agent><dc:title>' + \
		       holder + \
		       '</dc:title></Agent></dc:rights>\n'

		if 'type' in work_meta:
			out += '\t<dc:type rdf:resource="http://purl.org/dc/dcmitype/%s" />\n' % work_meta['type']
			
		if 'sourceurl' in work_meta:
			out += '\t<dc:source rdf:resource="%s" />\n' % (
				work_meta['sourceurl'])
		out += '\t<license rdf:resource="'+license+'" />\n'
		out += '</Work>\n'

	if license_rdf is not None:
		out += license_rdf + '\n'
	
	out += '</rdf:RDF>\n'
	
	return out

def generate_rdfa(files, license_name, license_url, verify_url):

	out = ''
	out +=  "<!-- Publish this file at " + verify_url + " -->\n"
	out += "<ul>\n"
	
	for f in files:
                h = fileHash(f)

		out += """<li>The file %s identified by <a href="magnet:?xt=urn:sha1:%s">urn:sha1:%s</a> is licensed to the public under the <a about="urn:sha1:%s" rel="license" href="%s">%s</a> license.</li>\n""" % (
			os.path.basename(f),
			h, h, h, license_url, license_name)

	out += '</ul>\n'
	
	return out
