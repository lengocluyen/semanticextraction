import os
import nltk
from nltk.corpus import WordNetCorpusReader

class WordNet(object):
    def __init__(self,wordnet, folder_path):
        self.wordnet = wordnet
        self.folder_path = folder_path

    def read_wordnet(self):
        cwd = os.getcwd()
        #nltk.data.path.append(cwd)
        wordnet_dir = "wordnet-1.6/"

        wn_path = "{0}/dict".format(wordnet_dir)
        self.wordnet = WordNetCorpusReader(os.path.abspath("{0}/{1}".format(cwd, wn_path)), nltk.data.find(wn_path))

    def synset2offset(self,ss):
        return str(ss.offset()).zfill(8)+"-"+ss.pos()

