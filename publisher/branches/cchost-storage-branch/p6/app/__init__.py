"""
p6.app

"""

import optparse

import interfaces
import wxpy
import extension

def getParser():
    """Configure and return an optparse option parser."""
    
    parser = optparse.OptionParser()
    parser.add_option("-l", "--locale", dest="locale", default=None,
                      help="Override the system locale.")
    
    
    return parser
