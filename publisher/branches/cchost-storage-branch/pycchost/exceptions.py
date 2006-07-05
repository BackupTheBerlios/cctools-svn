"""
pycchost.exceptions

A Python library which provides an interface for uploading files to
ccHost Installations
"""

class MissingParameterException(LookupError):
    pass

class SubmissionError(Exception):
    pass
    
class CommunicationsError(Exception):
    pass
