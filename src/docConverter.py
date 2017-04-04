from docx import opendocx, getdocumenttext
import os
from .directory import Directory

class DocConverter(object):
    def __init__(self):
        print ("Init class DocConverter")

    directory = Directory()

    def docx2text_fileInFolderConverter(self, dir, path):
        if self.directory.checkExistPath(path):
            self.directory.createPath(path)
        for name in dir:
            txtouput=path + self.directory.get_filename(name) + ".txt"
            self.docx2text_fileConverter(name,txtouput)
            print("Converted for " + txtouput)

    def docx2text_fileConverter(selft, docInput,txtOutput):
        try:
            document = opendocx(docInput)
            newfile = open(txtOutput, 'w')
        except:
            print(
                "Error in ", docInput
            )
            #exit()

        # Fetch all the text out of the document we just created
        paratextlist = getdocumenttext(document)

        # Make explicit unicode version
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode("utf-8"))

        # Print out text of document with two newlines under each paragraph
        newfile.write('\n\n'.join(newparatextlist))
