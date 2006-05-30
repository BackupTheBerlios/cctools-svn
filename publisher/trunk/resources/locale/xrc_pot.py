import sys
import libxml2

def writeHeader(outfile):
    """Write the PO file header to the specified file object"""

    header = """
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: Fri Feb 18 16:51:55 2005\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: ENCODING\\n"
"Generated-By: xrc_pot.py\\n"

"""

    outfile.write(header)

def extractIds(filename):
    result = []

    doc = libxml2.parseFile(filename)
    ctxt = doc.xpathNewContext()

    # extract the label list
    labels = ctxt.xpathEval('//label')

    for l in labels:
        result.append(l.content)

    ctxt = doc.xpathNewContext()

    # extract the label list
    labels = ctxt.xpathEval('//title')

    for l in labels:
        result.append(l.content)

    return result

if __name__ == '__main__':
   in_filename = sys.argv[-1]
   out_filename = ".".join( in_filename.split('.')[:-1] + ['pot'] )

   msg_ids = extractIds (in_filename)
   output = file(out_filename, 'w')

   writeHeader(output)

   for id in msg_ids:
      output.write ('msgid "%s"\n' % id)
      output.write ('msgstr ""\n\n')

   output.close()
