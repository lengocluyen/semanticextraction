import os
from SemanticExtraction.src.ATR.CandidateTriple import CandidateTriple
from SemanticExtraction.src.ATR.CoNLLXHandle import CoNLLXHandle
from SemanticExtraction.src.directory import Directory
import re

class TripleExtraction(object):
    #extraction triple from corpus around the terms

    def __init__(self, triple_list, stoptriples, corpus_path, pattern):
        self.triple_list = triple_list
        self.stoptriples = stoptriples
        self.corpus_path = corpus_path
        self.pattern = pattern

    def get_all_triple_from_all_file_corpus(self):
        conllx = CoNLLXHandle()
        directory = Directory()
        all_file_corpus = directory.scan_dir(self.corpus_path)
        count =0
        for file_corpus in all_file_corpus:
            print file_corpus
            count = count+1
            sentences = conllx.read_conllx(file_corpus)
            for sentence in sentences:
                self.get_all_triple_from_corpus_file(sentence)
        return count

    def get_all_triple_from_corpus_file(self,sentence):
        pos_tag_list = ""
        for token in sentence.words():
            pos_tag_list+=token.postag+"_"
        pos_tag_list = pos_tag_list.strip("_")
        pos_tag_list = pos_tag_list.replace("P+D","PPD")
        print pos_tag_list
        #resusult NN_PP_VB_CNN
        #print pos_tag_list
        self.extract_triple(pos_tag_list,sentence)

    def extract_triple(self,  pos_tag_sentence, sentence):

        for regex in self.pattern:
            #print pos_tag_sentence
            #print self.get_position_match_with_pattern(regex, pos_tag_sentence)
            triple_regex = self.pattern[regex]

            for position in self.get_position_match_with_pattern(regex, pos_tag_sentence):

                part1, part2, part2="","",""
                if position[0]>0:
                    part1 = pos_tag_sentence[0:position[0]-1].strip("_")
                part2 = pos_tag_sentence[position[0]:position[1]]
                #if position[1]<len(str):
                #   part3 = pos_tag_sentence[position[1]+1:len(str)].strip("_")
                triple=CandidateTriple("","","","","","")
                start = len(self.str_list_remove_null(part1.split("_")))
                end = start + len(self.str_list_remove_null(part2.split("_")))

                triple_all_regex = self.str_list_remove_null(triple_regex.split(':'))

                triple_subject_regex = triple_all_regex[0]
                triple_verbe_regex = triple_all_regex[1]

                end_subject = len(self.str_list_remove_null(triple_subject_regex.split("_"))) + start

                end_verbe = len(self.str_list_remove_null(triple_verbe_regex.split("_"))) + end_subject

                #print start, end_subject, end_verbe, end
                print start, end_subject, end_verbe, end

                for i in range(start, end):
                    #subject
                    if i <end_subject:
                        triple.subject =triple.subject +" " +sentence.words()[i].form
                        triple.subject_lemma = triple.subject_lemma + " " + sentence.words()[i].lemma
                    #verb
                    elif i>= end_subject and i < end_verbe:
                        triple.verb = triple.verb + " " + sentence.words()[i].form
                        triple.verb_lemma = triple.verb_lemma + " " + sentence.words()[i].lemma
                    #object
                    else:
                        triple.object = triple.object + " " + sentence.words()[i].form
                        triple.object_lemma = triple.object_lemma + " " + sentence.words()[i].lemma
               # print triple.subject +" bc "+ triple.verb +" object "+ triple.object
                #remove term with number
                #if self.has_numbers(term) is False and self.has_special_character(term) is False and self.is_exist_in_stoplist(term) is False:
                    #count = self.count_term_from_all_file_corpus(term_lemma)
                if self.is_exist_triple_in_list(triple) is False:
                        #candidateTerm = CandidateTerm(term, term_lemma, wordnet_connection.find_terms(term_lemma), count)  # check in existing Wordnet
                        self.triple_list.append(triple )

    def get_position_match_with_pattern(self, regex, pos_tag_sentence):
        #>>> pattern ="NN_NN+"
        #str="NN_NN_NN_CD_NN_NN_DD_NN"
        #[(m.start(0), m.end(0)) for m in re.finditer(pattern, str)]
        #[(0, 5), (12, 17)]
        regex_str = str(regex)
        return [(m.start(0), m.end(0)) for m in re.finditer(regex_str, pos_tag_sentence)]

    def str_list_remove_null(self, str_list):
        while( '' in str_list):
            str_list.remove('')
        return str_list

    def is_exist_triple_in_list(self, triple):
        for tr in self.triple_list:
            if tr.subject_lemma == triple.subject_lemma and tr.verb_lemma ==triple.verb_lemma and tr.object_lemma == triple.object_lemma:
                return True
        return False

    def to_string_and_file(self,filename):
        #if os.path.exists(filename):
        #os.remove(filename)
        file = open(filename,"w")
        self.sorted_triple_by_subject()
        #order
        new_triple_list = sorted(self.triple_list, key=lambda x: x.subject,reverse=True)
        for triple in new_triple_list:
            #candidate_term.term_lemma + "\n"
            file.write(triple.to_string()+"\n")
            print triple.to_string()
        file.close()

    def text(self, use_tokens=False, separator='\t'):
        """Return the text of the sentence."""
        if use_tokens:
            raise NotImplementedError('multi-word token text not supported.')
        else:
            return separator.join(t.form for t in self.triple_list)

    def has_numbers(self, str):
        return any(char.isdigit() for char in str)

    def is_exist_in_stoptriple(self,triple):
        for tr in self.stoptriples:
            if tr.subject_lemma == triple.subject_lemma and tr.verb_lemma ==triple.verb_lemma and tr.object_lemma == triple.object_lemma:
                return True
        return False

    def sorted_triple_by_subject(self):
        sorted(self.triple_list, key=lambda triple: triple.subject, reverse=True)