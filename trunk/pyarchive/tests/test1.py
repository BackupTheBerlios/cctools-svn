import pyarchive as pya
import pyarchive.submission as submission

submission = submission.ArchiveItem('barefootbrothers-genocide', 
                                        pya.const.OPENSOURCE_AUDIO, 
                                        pya.const.AUDIO, 
                                        'Genocide')
# submission['runtime'] = '5:20'
submission['license'] = 'http://creativecommons.org/licenses/by-sa/1.0/'

file1 = submission.addFile('GenocideHI.mp3',
                           pya.const.ORIGINAL,
                           pya.const.MP3_128K)

print submission.submit('nathan@yergler.net', '3210chs')
