import pyarchive as pya
import pyarchive.submission as submission

submission = submission.ArchiveItem('AbleFatFingers', 
                                        pya.const.OPENSOURCE_AUDIO, 
                                        pya.const.AUDIO, 
                                        'Fat Fingers')
submission['runtime'] = '5:00'
submission['license'] = 'http://creativecommons.org/licenses/by-sa/2.0/'

file1 = submission.addFile('ff.mp3')
file1.source = pya.const.ORIGINAL
file1.format = "192Kbps MP3"

print submission.submit('nathan@yergler.net', '3210chs')
