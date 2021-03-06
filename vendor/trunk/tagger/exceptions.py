"""
Copyright (c) 2004. Alastair Tse <acnt2@cam.ac.uk>
http://www-lce.eng.cam.ac.uk/~acnt2/code/pytagger/

Custom Exceptions
"""

__revision__ = "$Id$"

class ID3Exception(Exception):
	"""General ID3Exception"""
	pass

class ID3EncodingException(ID3Exception):
	"""Encoding Exception"""
	pass

class ID3VersionMismatchException(ID3Exception):
	"""Version Mismatch problems"""
	pass

class ID3HeaderInvalidException(ID3Exception):
	"""Header is malformed or none existant"""
	pass

class ID3ParameterException(ID3Exception):
	"""Parameters are missing or malformed"""
	pass

class ID3FrameException(ID3Exception):
	"""Frame is malformed or missing"""
	pass

class ID3NotImplementedException(ID3Exception):
	"""This function isn't implemented"""
	pass

