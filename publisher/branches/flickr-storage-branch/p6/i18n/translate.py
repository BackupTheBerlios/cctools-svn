import inspect

I18N_FILE = None

def dump_ (str_arg):
    """Dump strings for translation to one of two text files."""

    frame_info = inspect.getframeinfo(inspect.currentframe().f_back)

    src_file = frame_info[0]
    line_no = frame_info[1]
    
    if 'p6' in src_file:
        out_file = file('p6.txt', 'w+')
    else:
        out_file = file('ccpublisher.txt', 'w+')

    # write the translation record
    
    out_file.write(str_arg)
    out_file.write('\n')

    return str_arg

