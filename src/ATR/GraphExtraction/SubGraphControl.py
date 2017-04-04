from SemanticExtraction.src.ATR.CoNLLXHandle import CoNLLXHandle
from SemanticExtraction.src.ATR.CoNLLX.Sentence import Sentence
from SemanticExtraction.src.directory import Directory
from SubGraphAutoDetect import SubGraphAutoDetect
import os
import sys

class SubGraphControl(object):

    corpus=[]#collection de sentences in the file
    subject_patterns=[]#pattern for extracting the subject in sentence

    def __init__(self, path_outmap_corpus, path_subject_pattern):

        self.path_outmap_corpus = path_outmap_corpus
        self.path_subject_pattern = path_subject_pattern
        #adding the sentence to corpus
        self.get_corpus()
        #adding the subject pattern
        self.get_subject_patterns()
        print "Finish SubgraphControl Initialization"

    def extract_sub_graph_in_sentence(self):
        sub_graph_sentence_list=[]
        for sentences in self.corpus:
            for sentence in sentences:
                #class initialization
                sub_graph_auto_detect = SubGraphAutoDetect(self.subject_patterns,sentence)
                #call method extraction build_graph
                sub_graph_sentence = sub_graph_auto_detect.build_sub_graph()

                #read and add
                for item in sub_graph_sentence:
                    sub_graph_sentence_list.append(item)

        print "head"
        return sub_graph_sentence_list

    def get_subject_patterns(self):
        patterns = [line.rstrip('\n') for line in open(self.path_subject_pattern)]
        for item in patterns:
            if len(item)!=0:
                self.subject_patterns.append(item)

    def get_corpus(self):
        conllx = CoNLLXHandle()
        directory = Directory()
        all_file_corpus = directory.scan_dir(self.path_outmap_corpus)
        for file_corpus in all_file_corpus:
            sentences = conllx.read_conllx(file_corpus)
            self.corpus.append(sentences)

    def to_string(self, output_file, sub_graph_sentence_list):
        reload(sys)
        sys.setdefaultencoding('utf8')
        file = open(output_file, "w")
        for item in sub_graph_sentence_list:
            file.write(item.to_string())
            print item.to_string()
        file.close()