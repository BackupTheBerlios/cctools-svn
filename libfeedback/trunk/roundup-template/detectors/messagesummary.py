#$Id$

from roundup.mailgw import parseContent

def summarygenerator(db, cl, nodeid, newvalues):
    ''' If the message doesn't have a summary, make one for it.
    '''
    if newvalues.has_key('summary') or not newvalues.has_key('content'):
        return

    summary, content = parseContent(newvalues['content'], 1, 1)
    newvalues['summary'] = summary


def init(db):
    # fire before changes are made
    db.msg.audit('create', summarygenerator)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 38d7638272923ba22aa28342f267b611f3be392d
