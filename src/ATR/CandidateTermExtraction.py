# coding=utf-8
#import nltk.corpus
import os
import math
from SemanticExtraction.src.ATR.CandidateTerm import CandidateTerm
from SemanticExtraction.src.ATR.CoNLLXHandle import CoNLLXHandle
from SemanticExtraction.src.directory import Directory
import re
from SemanticExtraction.src.ATR.WordNetMongoDB import ConnectionMongoDB

class CandidateTermExtraction(object):
    #Extract Candidate Term by lenght of word and pattern
    #stopwords = nltk.corpus.stopwords.words('french')
    #terms={}
    def __init__(self, candidate_terme_list, stopwords, corpus_path, pattern):
        self.candidate_terme_list = candidate_terme_list
        self.stopwords = stopwords
        self.corpus_path = corpus_path
        self.pattern = pattern

    def get_all_term_from_all_file_corpus(self):
        conllx = CoNLLXHandle()
        directory = Directory()
        all_file_corpus = directory.scan_dir(self.corpus_path)
        count =0
        for file_corpus in all_file_corpus:
            count = count+1
            sentences = conllx.read_conllx(file_corpus)
            for sentence in sentences:
                self.get_all_terms_from_corpus_file(sentence)

        #calcul subfrequency
        self.calcul_field_subfrequency_in_candidate_term()
        #calcul sub other term nested
        self.calcul_field_other_sub_frequency_in_candidate_term()
        #calcul cvalue
        self.calcul_c_value_for_candidate_term()
        return count

    def get_all_terms_from_corpus_file(self,sentence):
        pos_tag_list = ""
        sent =""
        for token in sentence.words():
            token.postag = token.postag.replace("+","P")
            pos_tag_list+=token.postag+"_"
            sent+=token.form+"_"
        pos_tag_list = pos_tag_list.strip("_")
        sent = sent.strip("_")
        #pour le test
        filename = "/home/lengocluyen/Data/sample/strucutre.txt"
        file =  open(filename,"a")
        file.write(sent + "\n")
        file.write(pos_tag_list +"\n")
        file.close()
        #resusult NN_PP_VB_CNN
        #print pos_tag_list
        self.extract_term(pos_tag_list,sentence)

    def get_position_match_with_pattern(self, regex, pos_tag_sentence):
       #>>> pattern ="NN_NN+"
       #str="NN_NN_NN_CD_NN_NN_DD_NN"
        #[(m.start(0), m.end(0)) for m in re.finditer(pattern, str)]
        #[(0, 5), (12, 17)]
        return [(m.start(0), m.end(0)) for m in re.finditer(regex, pos_tag_sentence)]

    def extract_term(self,  pos_tag_sentence, sentence):
        for regex in self.pattern:
            #print regex
            #print pos_tag_sentence
            #print self.get_position_match_with_pattern(regex, pos_tag_sentence)

            for position in self.get_position_match_with_pattern(regex, pos_tag_sentence):

                part1, part2, part2="","",""
                if position[0]>0:
                    part1 = pos_tag_sentence[0:position[0]-1].strip("_")
                part2 = pos_tag_sentence[position[0]:position[1]]
                #if position[1]<len(str):
                #   part3 = pos_tag_sentence[position[1]+1:len(str)].strip("_")
                term=""
                term_lemma=""
                start = len(self.str_list_remove_null(part1.split("_")))
                end = start + len(self.str_list_remove_null(part2.split("_")))

                for i in range(start, end):
                    term = term +" " +sentence.words()[i].form
                    term_lemma = term_lemma + " "+ sentence.words()[i].lemma
                term = term.strip(" ")
                term_lemma = term_lemma.strip(" ")

                #remove term with number
                if self.has_numbers(term) is False and self.has_special_character(term) is False and self.is_exist_in_stoplist(term) is False:
                    count = self.count_term_from_all_file_corpus(term_lemma)
                    if self.is_exist_terms(term_lemma) is False:
                        #print term_lemma
                        #wordnet_connection = ConnectionMongoDB()
                        #wordnet_connection.find_terms(term_lemma)
                        candidateTerm = CandidateTerm(term, term_lemma, 0 , count)  # check in existing Wordnet
                        self.candidate_terme_list.append(candidateTerm)


    def str_list_remove_null(self, str_list):
        while( '' in str_list):
            str_list.remove('')
        return str_list

    def calcul_field_subfrequency_in_candidate_term(self):
        for candidateTerm in self.candidate_terme_list:
            term_lemma = candidateTerm.term_lemma
            supterms = self.frequency_sub_terms_in_exists_list_candidate(term_lemma)
            candidateTerm.subfrequence = len(supterms)
            candidateTerm.supterms = supterms


    def frequency_sub_terms_in_exists_list_candidate(self, subterm_lemma):
        supterms=[]
        for item in self.candidate_terme_list:
            term_lemma = item.term_lemma
            if subterm_lemma in term_lemma and subterm_lemma is not term_lemma:
                supterms.append(term_lemma)
        return supterms

    def calcul_field_other_sub_frequency_in_candidate_term(self):
        for candidateTerm in self.candidate_terme_list:
            term_lemma = candidateTerm.term_lemma
            subterms = self.count_frequency_other_terms_exists_list_candidate(term_lemma)
            candidateTerm.subterms= subterms

    def count_frequency_other_terms_exists_list_candidate(self, term_lemma):
        subterms = []
        for item in self.candidate_terme_list:
            subterm_lemma = item.term_lemma
            if subterm_lemma in term_lemma and subterm_lemma is not term_lemma:
                subterms.append(subterm_lemma)
        return subterms

    def count_term_from_all_file_corpus(self, term):
        conllx = CoNLLXHandle()
        directory = Directory()
        all_file_corpus = directory.scan_dir(self.corpus_path)
        count =0
        for file_corpus in all_file_corpus:
            count += self.count_term_from_file_corpus(term, conllx.read_conllx(file_corpus))
        return count

    def count_term_from_file_corpus(self, term, sentences):
        """Count terms in every corpus file -> limited the used memory"""
        count = 0
        for sentence in sentences:
            count +=sentence.to_normal_sentence().count(term)
        return count

    def calcul_c_value_for_candidate_term(self):
        cvalue=0
        for candidate_Term in self.candidate_terme_list:
            if candidate_Term.subfrequence == 0:
                number_of_words = len(candidate_Term.term.split())
                cvalue = self.log2( number_of_words*int(candidate_Term.frequence))
                #cvalue = log2|a|.f(a)
            else:
                #cvalue = log2|a|.(f(a)-(1/P(T(a)))*f(b))
                #value = candidate_Term.frequence - ((1/candidate_Term.othersubfrequence)*candidate_Term.subfrequence)
                PTa = len(candidate_Term.supterms)
                fb = 0
                for subterm in candidate_Term.subterms:
                    frequence = self.get_candidate_term_by_lemma(subterm).frequence
                    fb = fb + frequence
                number_of_words = len(candidate_Term.term.split())

                print str(candidate_Term.frequence) + "- ((1/"+str(PTa)+"+)*"+str(fb)+")"
                value =  (1/PTa)*fb
                result = number_of_words*(abs(candidate_Term.frequence-value))
                if result ==0:
                    cvalue =0
                else:
                    cvalue = self.log2(result)
            candidate_Term.cvalue = cvalue



    def get_candidate_term_by_lemma(self,term_lemma):
        result = None
        for term in self.candidate_terme_list:
            if term.term_lemma == term_lemma:
                result=term
        return result

    def log2(self, x):
        print x
        return math.log(x,2)

    def is_exist_terms(self, terms):
        for t in self.candidate_terme_list:
            if terms==t.term_lemma:
                return True
        return False

    def to_string(self,filename):
        #if os.path.exists(filename):
        #os.remove(filename)
        file = open(filename,"w")
        self.sorted_candidate_term()
        #order
        new_candidate_term_list = sorted(self.candidate_terme_list, key=lambda x: x.frequence,reverse=True)
        for candidate_term in new_candidate_term_list:
            #candidate_term.term_lemma + "\n"
            file.write(candidate_term.term + "\t\t\t\t\t" + candidate_term.term_lemma +"\t\t\t\t\t"+ str(candidate_term.frequence) +"\t\t\t\t\t" +str(candidate_term.wordnet) +"\t\t\t\t\t" +str(candidate_term.subfrequence)+"\t\t\t\t\t" +str(candidate_term.subterms)+"\t\t\t\t\t" +str(candidate_term.supterms)+"\t\t\t\t\t" +str(candidate_term.cvalue)+"\n")
            print candidate_term.term + "\t\t\t\t\t" + candidate_term.term_lemma +"\t\t\t\t\t"+ str(candidate_term.frequence) +"\t\t\t\t\t" +str(candidate_term.wordnet)+"\t\t\t\t\t" +str(candidate_term.subfrequence)+"\t\t\t\t\t" +str(candidate_term.subterms)+"\t\t\t\t\t" +str(candidate_term.supterms)+"\t\t\t\t\t" +str(candidate_term.cvalue)+"\n"
        file.close()

    def text(self, use_tokens=False, separator='\t'):
        """Return the text of the sentence."""
        if use_tokens:
            raise NotImplementedError('multi-word token text not supported.')
        else:
            return separator.join(t.form for t in self.candidate_terme_list)

    def has_numbers(self, str):
        return any(char.isdigit() for char in str)

    def has_special_character(self,str):
        if set('[€~!@#$%^&*()_+{}":;]+$').intersection(str) or len(str)<3:
            return True
        return False

    def is_exist_in_stoplist(self,term):
        for word in self.stopwords:
            if term == word:
                return True
        return False

    def sorted_candidate_term(self):
        sorted(self.candidate_terme_list, key=lambda terms: terms.term)