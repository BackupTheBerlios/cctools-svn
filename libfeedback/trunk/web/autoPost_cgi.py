#!/usr/local/python241/bin/python

import os
import ConfigParser

import cgi

import roundup
import roundup.instance
import roundup.password

TRACKER_HOME = '/web/roundup/trackers/ccpublisher'
TRACKER_USER = 'nathan'

DEFAULT_PRIORITY = 'critical'
DEFAULT_TITLE = 'Autoreported crash information'

DEFAULT_KEYWORD = 'autoreport'

# a user who watches for new auto-submitted issues
# and is added to their initial nosy list;
# set to None to disable this feature
WATCH_USER = 'admin'

def findNode(roundupClass, filter):
    for id in roundupClass.list():
        for key in filter:
            if not(roundupClass.getnode(id)[key] == filter[key]):
                # this isn't what we're looking for
                continue

            # we passed all keys -- this is it
            return roundupClass.getnode(id)

    # we didn't find it -- return none
    return None

def createIssue(db, title, priority, application, platform,
                nosy=[], messages=[], topics=[]):

    # create a new issue in Roundup
    issues = db.getclass('issue')
    issue_id = issues.create(
                  title=title,
                  priority=priority,
                  application=application,
                  platform=[platform],
                  messages=messages,
                  nosy=nosy,
		  topic=topics
                  )

    db.commit()

    # return the id of the new issue
    return issue_id

def cgiIssue(formFields):
    """Parse issue fields from the a CGI FieldStorage instance and create
    the new issue in a Roundup tracker."""
    
    # open the roundup tracker configuration file
    trackerConfig = ConfigParser.ConfigParser()
    trackerConfig.read(os.path.join(TRACKER_HOME, 'config.ini'))
    
    # open the roundup database
    r_instance = roundup.instance.open(TRACKER_HOME)
    r_db = r_instance.open(TRACKER_USER)

    # get handles to things like priority, etc
    title = (formFields.has_key('title') and formFields['title']) or \
            DEFAULT_TITLE
    
    priority = findNode(r_db.getclass('priority'),
                        {'name':(formFields.has_key('priority') and formFields['priority']) or DEFAULT_PRIORITY})['id']

    application = findNode(r_db.getclass('application'),
                           {'identifier': formFields['app_id'],
                            'version'   : formFields['app_version']})['id']

    platform = findNode(r_db.getclass('platform'),
                        {'identifier': formFields['platform']})
    if platform is None:
        # create the new platform, assuming 
	p_id = formFields['platform']
        platform = r_db.getclass('platform').\
                   create(identifier=p_id, supported=True)
    else:
        # just get the ID
        platform = platform['id']

    if WATCH_USER is not None:
        nosy = [findNode(r_db.getclass('user'),
                         {'username': WATCH_USER})['id']]
    else:
        nosy = []

    # get a handle to a default keyword we want to assign
    if DEFAULT_KEYWORD is not None:
        topics = [findNode(r_db.getclass('keyword'),
	                   {'name':DEFAULT_KEYWORD})['id']]
    else:
        topics=[]

    # add any notes to the issue as a message
    messages = []
    m_class = r_db.getclass('msg')

    if formFields.has_key('message'):
        msgs = formFields['message']
        
        # there may be one or more messages to create
        try:
            msgs.append(None)
            del msgs[-1]
        except:
            msgs = [msgs]

        for m in msgs:
            messages.append(m_class.create(content=m))
            
            
    issue_id = createIssue(r_db, title, priority, application,
                           platform, nosy, messages, topics)

    return '%sissue%s' % (trackerConfig.get('tracker', 'web'),
                              issue_id)

def autoReporter (environ, start_response):
    """A simple WSGI-compliant application which takes values provided
    by an auto-reporter and inserts them into the Roundup database,
    returning the URL of the created issue."""
    
    fields = paste.request.parse_formvars(environ)
    
    if environ['REQUEST_METHOD'] == 'POST':
        response = cgiIssue(fields)

        start_response('200 OK', [('content-type', 'text/plain')])
        return [response]
        
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ['<html><title>Sample Report Interface</title><body>',
                '<form method="POST">',
                'Title (optional): <input type="text" name="title" /><br/>',
                'App ID: <input type="text" name="app_id" /><br/>',
                'App Version: <input type="text" name="app_version" /><br/>',
                'Platform: <input type="text" name="platform" /><br/>',
                'Message 1: <input type="text" name="message" /><br/>',
                'Message 2: <input type="text" name="message" /><br/>',
                '<input type="submit" /></form>',
                '</body></html>']


if __name__ == '__main__':
    form = cgi.FieldStorage()

    # create a dictionary
    qs = {}
    for key in form.keys():
       qs[key] = form.getvalue(key)

    print "Content-type: text/plain"
    print

    print cgiIssue(qs)

