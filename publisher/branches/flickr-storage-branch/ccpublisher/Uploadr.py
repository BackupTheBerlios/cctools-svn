#!/usr/bin/env python

import sys, time, os, urllib2, shelve, string, xmltramp, mimetools, mimetypes, md5, webbrowser, traceback
#
#   Requires:
#       xmltramp http://www.aaronsw.com/2002/xmltramp/
#       flickr account http://flickr.com
#
#Most credit goes to: Cameron Mallory
#Minor changes to include with ccPublisher made by Robert Litzke
#   This code has been updated to use the new Auth API from flickr.
#
#   You may use this code however you see fit in any form whatsoever.
#
#
# Location to scan for new images 
#
#   Flickr settings
#
FLICKR = {"title": "",
        "description": "",
        "tags": "auto-upload",
        "is_public": "1",
        "is_friend": "0",
        "is_family": "0" }

##
##  You shouldn't need to modify anything below here
##
FLICKR["secret" ] = "367567149e034a21"#"d8fb77bee73ab91b"
FLICKR["api_key" ] = "6777b9af9f7b864b95f67c91e2c07310"#"2b22d953d654eb9e9ad25801238b4049"
class APIConstants:
    base = "http://flickr.com/services/"
    rest   = base + "rest/"
    auth   = base + "auth/"
    upload = base + "upload/"
    
    token = "auth_token"
    secret = "secret"

    key = "api_key"
    sig = "api_sig"
    frob = "frob"
    perms = "perms"
    method = "method"
    licenseid = "license_id"
    photoid = "photo_id"    
    
    
    def __init__( self ):
       pass
    

class Uploadr:
    token = None
    perms = ""
    TOKEN_FILE = ".flickrToken"
    
    def __init__( self ):
        self.token = self.getCachedToken()
        self.api = APIConstants()



    """
    Signs args via md5 per http://www.flickr.com/services/api/auth.spec.html (Section 8)
    """
    def signCall( self, data):
        keys = data.keys()
        keys.sort()
        foo = ""
        for a in keys:
            foo += (a + data[a])
        
        f = FLICKR[ self.api.secret ] + self.api.key + FLICKR[ self.api.key ] + foo
        print "TEMP SIGNED DATA:  "+f
        return md5.new( f ).hexdigest()
   
    def urlGen( self , base,data, sig ):
        foo = base + "?"
        for d in data: 
            foo += d + "=" + data[d] + "&"
        return foo + self.api.key + "=" + FLICKR[ self.api.key ] + "&" + self.api.sig + "=" + sig
        
    def genLicense( self , base, pho, lic, sig, tok ):
        foo = base + "?"
        foo+="method=flickr.photos.licenses.setLicense&"
        foo += self.api.key + "=" + FLICKR[ self.api.key ] + "&" + self.api.photoid + "=" + str(pho)
        foo += "&" + self.api.licenseid + "=" + str(lic) + "&" + self.api.token + "=" + str(tok) #+ "&" +self.api.sig + "=" + sig
        return foo
 
    """
    Authenticate the application, and store token
    """
    def authenticate( self ):
        print "Authenticating"
        self.getFrob()
        self.getAuthKey()
    
    """
    Since we can't be sure if ccPublisher stores authentication information by caching the Token,
    we must run this section every time we use the application, right before uploading images
    """
    def authenticatePt2( self ):
        self.getFrob()
        self.getToken()   
        self.cacheToken()
    """
    flickr.auth.getFrob
    
    Returns a frob to be used during authentication. This method call must be 
    signed.
    
    This method does not require authentication.
    Arguments
    
   self.api.key (Required)
    Your API application key. See here for more details.     
    """
    def getFrob( self ):
        print "getFrob"
        d = { 
            self.api.method  : "flickr.auth.getFrob"
            }
        sig = self.signCall( d )
        url = self.urlGen( self.api.rest, d, sig )
        try:
            response = self.getResponse( url )
            if ( self.isGood( response ) ):
                FLICKR[ self.api.frob ] = str(response.frob)
            else:
                self.reportError( response )
        except:
            print "Error getting frob:" , str( sys.exc_info() )


    """
    Checks to see if the user has authenticated this application
    """
    def getAuthKey( self ): 
        d =  {
            self.api.frob : FLICKR[ self.api.frob ], 
            self.api.perms : "write"  
            }
        sig = self.signCall( d )
        url = self.urlGen(self.api.auth, d, sig )
        try:
            webbrowser.open( url )
        except:
            print str(sys.exc_info())  

    """
    http://www.flickr.com/services/api/flickr.auth.getToken.html
    
    flickr.auth.getToken
    
    Returns the auth token for the given frob, if one has been attached. This method call must be signed.
    Authentication
    
    This method does not require authentication.
    Arguments
    
    NTC: We need to store the token in a file so we can get it and then check it insted of
    getting a new one all the time.
        
    self.api.key (Required)
       Your API application key. See here for more details.
    frob (Required)
       The frob to check.         
    """   
    def getToken( self ):
        print "getToken"
        d = {
           self.api.method : "flickr.auth.getToken",
           self.api.frob : str(FLICKR[self.api.frob ])
        }
        sig = self.signCall( d )
        url = self.urlGen(self.api.rest, d, sig )
        try:
            res = self.getResponse( url )
            if ( self.isGood( res ) ):
                self.token = str(res.auth.token)
                self.perms = str(res.auth.perms)
                self.cacheToken()
            else :
                self.reportError( res )
        except:
            print str( sys.exc_info() )

    """
    Attempts to get the flickr token from disk.
    """
    def getCachedToken( self ): 
        if ( os.path.exists( self.TOKEN_FILE )):
            return open( self.TOKEN_FILE ).read()
        else :
            return None
        


    def cacheToken( self ):
        print "cacheToken"
        try:
            open( self.TOKEN_FILE , "w").write( str(self.token) )
        except:
            print "Issue writing token to local cache " , str(sys.exc_info())

    """
    flickr.auth.checkToken

    Returns the credentials attached to an authentication token.
    Authentication
    
    This method does not require authentication.
    Arguments
    
   self.api.key (Required)
        Your API application key. See here for more details.
    auth_token (Required)
        The authentication token to check. 
    """
    def checkToken( self ):    
        if ( self.token == None ):
            return False
        else :
            d = {
               self.api.token  :  str(self.token) ,
               self.api.method :  "flickr.auth.checkToken"
            }
            sig = self.signCall( d )
            url = self.urlGen(self.api.rest, d, sig )     
            try:
                res = self.getResponse( url ) 
                if ( self.isGood( res ) ):
                    self.token = res.auth.token
                    self.perms = res.auth.perms
                    return True
                else :
                    self.reportError( res )
            except:
                print str( sys.exc_info() )          
            return False
    


    #
    #
    # build_request/encode_multipart_formdata code is from www.voidspace.org.uk/atlantibots/pythonutils.html
    #
    #
    def build_request(self, theurl, fields, files, txheaders=None):
        """
        Given the fields to set and the files to encode it returns a fully formed urllib2.Request object.
        You can optionally pass in additional headers to encode into the opject. (Content-type and Content-length will be overridden if they are set).
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.    
        """
        content_type, body = self.encode_multipart_formdata(fields, files)
        if not txheaders: txheaders = {}
        txheaders['Content-type'] = content_type
        txheaders['Content-length'] = str(len(body))

        return urllib2.Request(theurl, body, txheaders)     

    def encode_multipart_formdata(self,fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
        """ Encodes fields and files for uploading.
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        Return (content_type, body) ready for urllib2.Request instance
        You can optionally pass in a boundary string to use or we'll let mimetools provide one.
        """    
        CRLF = '\r\n'
        L = []
        if isinstance(fields, dict):
            fields = fields.items()
        for (key, value) in fields:   
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % filetype)
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY        # XXX what if no files are encoded
        return content_type, body
    
    
    def isGood( self, res ):
        if ( not res == "" and res('stat') == "ok" ):
            return True
        else :
            return False            
            
    def reportError( self, res ):
        try:
            print "Error:", str( res.err('code') + " " + res.err('msg') )
        except:
            print "Error: " + str( res )

    """
    Send the url and get a response.  Let errors float up
    """
    def getResponse( self, url ):
        xml = urllib2.urlopen( url ).read()
        return xmltramp.parse( xml )
    
    def setLicense( self, photoid, licenseid ):
        print "setting license"
        d= {
            self.api.method : "flickr.photos.licenses.setLicense",
            self.api.photoid : str(photoid),
            self.api.licenseid : str(licenseid)
            }
        sig = self.signCall( d )
        url = self.genLicense( self.api.rest, photoid, licenseid, sig, self.token)
        print "URL:"+url
        try:
            response=self.getResponse( url )
            print response
            if ( self.isGood( response ) ):
                print "SUCCESS!!"
            else:
                print "FAILED"
        except:
            exc, val, tb = sys.exc_info()
            logfile = open("uploadrlog.txt", "a")
            traceback.print_exception(exc, val, tb, file=logfile)
            logfile.close()
            del tb    
    def uploadImage( self, image, title=None, desc=None,tags=None ):
        if ( 0==0 ):#not self.uploaded.has_key( image ) ):
            print "Uploading ", image , "...",
            try:
                photo = ('photo', image, open(image,'rb').read())
                d = {
                   self.api.token   : str(self.token),
                   self.api.perms   : str(self.perms),
                    "title"     : str( title ),
                    "description": str( desc ),
                    "tags"      : str( tags ),
                    "is_public" : str( FLICKR["is_public"] ),
                    "is_friend" : str( FLICKR["is_friend"] ),
                    "is_family" : str( FLICKR["is_family"] )
                }
                sig = self.signCall( d )
                d[ self.api.sig ] = sig
                d[ self.api.key ] = FLICKR[ self.api.key ]        
                url = self.build_request( self.api.upload, d, (photo,))    
                xml = urllib2.urlopen( url ).read()
                res = xmltramp.parse(xml)
                if ( self.isGood( res ) ):
                    #print "successful."
                    #print 'SIG:'+sig
                    #print 'API KEY:'+FLICKR[self.api.key ]
                    self.setLicense(res.photoid, 2)
                else :
                    print "problem..."
                    self.reportError( res )
            except:
                print str(sys.exc_info())
