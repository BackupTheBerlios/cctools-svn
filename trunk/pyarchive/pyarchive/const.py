"""
pyarchive.

copyright 2004, Creative Commons, Nathan R. Yergler
"""

__id__ = "$Id$"
__version__ = "$Revision$"
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'

# source options
ORIGINAL = 'original'
DERIVITAVE = 'derivative'

# media types
AUDIO = 'audio'
MOVIE = VIDEO = 'movies'

# collection names
OPENSOURCE_AUDIO = 'opensource_audio'

# meta keywords
VALID_META = {}

DATE = 'date'
PRODUCER = 'producer'
PROD_COMPANY = 'production_company'
DIRECTOR = 'director'
CONTACT = 'contact'
SPONSOR = 'sponsor'
DESC = 'description'
RUNTIME = 'runtime'
COLOR = 'color'
SOUND = 'sound'
SHOTLIST = 'shotlist'
SEGMENTS = 'segments'
CREDITS = 'credits'
COUNTRY = 'country'

CREATOR = 'creator'
TAPER = 'taper'
SOURCE = 'source'
NOTES = 'notes'

VALID_META[MOVIE] = [DATE, PRODUCER, PROD_COMPANY, DIRECTOR, CONTACT, SPONSOR,
                      DESC, RUNTIME, COLOR, SOUND, SHOTLIST, SEGMENTS, CREDITS,
                      COUNTRY]

VALID_META[AUDIO] = [CREATOR, DESC, TAPER, SOURCE, RUNTIME, DATE, NOTES]

# files keywords
FORMAT = 'format'

# RUNTIME is also for files metadata

# format names
WAVE = 'WAVE'
MP3_64K = '64Kbps MP3'
MP3_128K = '128Kbps MP3'
MP3_256K = '256Kbps MP3'
MP3_VBR = 'VBR MP3'
MP3_96K = '96Kbps MP3'
MP3_160K = '160Kbps MP3'
MP3_192K = '192Kbps MP3'
OGG_VORBIS = 'Ogg Vorbis'
SHORTEN = 'Shorten'
FLAC = 'Flac'
FLAC_24b = '24bit Flac'
M3U_64K = '64Kbps M3U'
M3U_VBR = 'VBR M3U'
MP3_64K_ZIP = '64Kbps MP3 ZIP'
VBR_ZIP = 'VBR ZIP'
SHORTEN_ZIP = 'Shorten ZIP'
FLAC_ZIP = 'Flac ZIP'
CHECKSUMS = 'Checksums'
MPEG2 = 'MPEG2'
MPEG1 = 'MPEG1'
MPEG4_64K = '64Kb MPEG4'
MPEG4_256K = '256Kb MPEG4'
MPEG4 = 'MPEG4'
QT_56K = '56Kb QuickTime'
QT_64K = '64Kb QuickTime'
QT_256K = '256Kb QuickTime'
QT = 'QuickTime'
DIVX = 'DivX'
IV50 = 'IV50'
WINDOWS_MEDIA = 'Windows Media'
CINEPACK = 'Cinepack'
ANIM_GIF = 'Animated GIF'
THUMBNAIL = 'Thumbnail'
JPEG = 'JPEG'
TIFF_SINGLE_ORIG = 'Single Page Original TIFF'
TIFF_SINGLE_PROC = 'Single Page Processed TIFF'
TIFF_MULTI_ORIG = 'Multi Page Original TIFF'
TIFF_MULTI_PROC = 'Multi Page Processed TIFF'
DJVU = 'DjVu'
TEXT = 'Text'
TEXT_PAGE = 'Single Book Page Text'
TEXT_TGZ = 'TGZiped Text Files'
BOOK_COVER = 'Book Cover'
DAT = 'DAT'
ARC = 'ARC'
META = 'Metadata'
FILES_META = 'Files Metadata'
ITEM_META = 'Item Metadata'
BOOK_META = 'Book Metadata'
