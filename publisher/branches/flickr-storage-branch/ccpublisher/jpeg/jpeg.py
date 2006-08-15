"""Extract and save a JPG comments or exif segment """

## JPEG data is divided into segments, each of which starts with a 2-byte marker.
## The first byte of each marker is FF. The second byte defines the type of marker.
## In a header the marker is immediately followed by two bytes that indicate the length of the information, 
## in bytes, that the header contains.  
## The two bytes that indicate the length are always included in that count.
##
## ## To allow for recovery in the presence of errors, it must be possible to detect markers without 
## ## decoding all of the intervening data. Hence markers must be unique. 
## ## To achieve this, if an FF byte occurs in the middle of a segment, an extra 00 stuffed byte is 
## ## inserted after it and 00 is never used as the second byte of a marker. 

## Usefull Markers:
## SOI  - start of image         (FFD8) - if file does not start with this, it's not JPEG
## APP0                          (FFE0)
## APP1 - EXIF segment           (FFE1) - metadata like: description, date/time taken, author, camera details
## APP2 - EXIF extension         (FFE2)   photo quality details, GPS details, thumbnail etc 
##                                      - many cameras store info here, some apps store to, more just read
##                                      - it is however a kind of complex data structure
## COM  - comments segment       (FFFE) - I'm not sure how many applications use this, Photoshop doesn't seem to
##                                      - Jpegs can have multiple comments, but for now only read
##                                        the first one (most jpegs only have one anyway). Comments
##                                        are simple single byte ISO-8859-1 strings.
## APP13 - IPTC segment          (FFED) - another metadata segment (Photoshop & Picasa image caption)
##                                      - captions, keywords, people, ratings, etc.
## SOF  - Start of Frame segment (FFC0) - the actual image

import util
import exif

__version__ ="0.1.3"
__license__ = "python"

DEBUG = False

class NoImageFound(Exception): pass
class NoJPEGFound(Exception): pass


def _read(file, marker):
    "return value of <marker> segment if exists, or None otherwise"
    segmentValue=None
    try: markerSeg, sof, length, im = _process(file, marker)
    except: return ""
    if markerSeg:
        im.seek(-2, 1)  #retract right after marker ID
        segmentValue = im.read(util.getNr(length))[2:]
    im.close()
    if not markerSeg and not sof:
        raise NoImageFound, "There is no image in this image file ?"
    return segmentValue

def _write(value, file, marker):
    """-Overwrights <marker> segment with given <value>
       -if <marker> segment does not already exist then it will write it 
        right before the image segment (SOF - FFC0)
    """
    markerSeg, sof, length, im = _process(file, marker)
    if markerSeg or sof:
        lenHex = util.setNr(len(value)+2, "short")      #the length on 2 bytes
        segment = "\xFF" + marker + lenHex + value  #segment = marker + value length + value
        
        pos = im.tell() - 4 
        im.seek(0)
        before = im.read(pos)
        if markerSeg: 
            im.seek(util.getNr(length) + 2, 1)     #skip over existing segment, including marker
        after = im.read()
        im.close()
        im = open(file, "wb")
        im.write(before)
        im.write(segment)
        im.write(after)
        im.close()
    else:
        im.close()
        raise NoImageFound, "There is no image in this image file ?"

def _process(file, target):
    """seek target marker in JPEG file, and return tuple:
    (found marker segment boolean, reached image segment boolean, marker segment length, 
    the open file object positioned at the begining of value)
    """
    comment = image = False
    im = open(file, "rb")
    marker = im.read(2)
    if marker != "\xFF\xD8":
        raise NoJPEGFound, "Not a JPEG image"
    l=2
    while im.read(1) == "\xFF":
        markerType = im.read(1)
        length = im.read(2)
        l += util.getNr(length) + 2
        if markerType == "\xC0": #SOF - got to the image, stop
            return (False, True, length, im) 
        if markerType == target: 
            return (True, False, length, im) 
        #skip over current segment 
        #-2 to move <length> positions starting right after marker
        im.seek(util.getNr(length) - 2, 1)  
    return (False, False, length, im) 
     
# COM segment - FFFE - a segment to be used for whatever 
def getComments(file):
    "read comments (\xFF\xFE COM segment) from a JPEG file"
    com = _read(file, "\xFE")
    if com is not None:
        return com
    return ""

def setComments(txt, file):
    "write a comment (\xFF\xFE COM segment) into a JPEG file"
    return _write(txt, file, "\xFE")

def getExif(file):
    "return FFE1 Exif segment (APP1) from a JPEG file, wrapped into an Exif instance object"
    exifSeg = _read(file, "\xE1")
    if exifSeg is not None:
        return exif.Exif(exifSeg)
    
def setExif(exif, file):
    "write an exif (\xFF\xE1 Exif segment) segment into a JPEG file, where <exif> must be an Exif instance object"
    return _write(exif.binary(), file, "\xE1")

def getExif2(file):  #extended
    "return FFE2 extended Exif segment (APP2) from a JPEG file, wrapped into an Exif instance object"
    exifSeg = _read(file, "\xE2")
    if exifSeg is not None:
        return exif.Exif(exifSeg)
    
def setExif2(exif, file):
    "write an extended exif (\xFF\xE2 Exif segment) segment into a JPEG file, where <exif> must be an Exif instance object"
    return _write(exif.binary(), file, "\xE2")


##IPTC:
## http://www.iptc.org/IIM/
## http://www.controlledvocabulary.com/imagedatabases/iptc_naa.html
##
## also see Exiv2 C++ app: http://home.arcor.de/ahuggel/exiv2/iptc.html
## Const Byte Jpegbase::App13_  = 0Xed;        - iptc here
## Const Uint16_T Jpegbase::Iptc_ = 0X0404;
##
## iptc.cpp ::READ (LINE 152)
## dataset marker 1 byte   0x1C
## record         1 byte
## dataset        1 byte
##
## if next byte is 0x08 then this is extended dataset:
##     pass
## otherwise is standard:
##     dataset len    short    (big endian)
    

def test(debug=True):
    global DEBUG
    debugorig = DEBUG
    DEBUG = debug
    import os
    folder = r"C:\test"
    files = [file for file in os.listdir(folder) if file.lower().endswith(".jpg")]
    tags = {}
    for file in files:
        print file.ljust(40)
        try:
            e1 = getExif(os.path.join(folder, file))
            e2 = getExif2(os.path.join(folder, file))
        except Exception, e:
            print str(e) 
            continue
        do = []
        if e1 is not None:
            print "has exif", 
            do.append(e1)
        if e2 is not None:
            print "has exif2", 
            do.append(e2)
        cnt=0
        for e in do:
            for ifd in e.ifds:
                for tag in ifd:
                    cnt += 1
                    id = tag.niceID()
                    old = tags.get(id, (0,0,0))
                    if e is e1:
                        tags[id] = (old[0] + 1, old[1] + 1, old[2])
                    else:
                        tags[id] = (old[0] + 1, old[1], old[2] + 1)
        print cnt
    keys = [(tags[k][0], k) for k in tags]
    keys.sort()
    keys.reverse()
    keys = [k for _,k in keys]
    print "decending sorted tags, by count"
    for key in keys:
        print key.ljust(30), "count", tags[key][0], "e1 count", tags[key][1], "e2 count", tags[key][2]
    DEBUG = debugorig