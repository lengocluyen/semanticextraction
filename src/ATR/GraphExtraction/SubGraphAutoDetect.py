import re
import math
from SemanticExtraction.src.ATR.DataStructure.SubGraphSentence import SubGraphSentence

import sys
'''
Approche d'utilisation de motif
comment defini un motif?
N (suj) -> V <- N (obj) ??
:suject -> V ->
Approche d'actraction automatique
+ Utiliser Pos Tagging
+ Trouver la verbe principale qui est correspondance avec le root dans l'arbre d'etiquetage
+ Trouver le subjet qui est correspondance avec la verbe. Ici, L'ID du Verbe est le HEAD du suject
+ Touver les objects qui sont correspondances avec les objects apres la verbe principle. Attention: Objects ici, sont une liste qui inclure aux a-objet, p-objet, de-objet_
'''
class SubGraphAutoDetect(object):

    #variables
    def __init__(self, subject_patterns, sentence):
        self.subject_patterns = subject_patterns
        self.sentence = sentence
        print "Finish SubGraphAutoDetect Initialization!"


    def build_sub_graph(self):
        #return to sub_graph_sentence
        sub_graph_sentence_list=[]
        print "Extracting Verb"
        verbe_element = self.verbe_extract() #return an element
        if verbe_element is not None:
            subjet_list = self.subjects_extract(verbe_element,self.subject_patterns) #return an element
            object_list = self.object_extract(verbe_element,self.subject_patterns)
            if len(subjet_list)>0:
            #   for sujet in subjet_element:
                for sujet in subjet_list:
                    sub_graph_sentence = SubGraphSentence(sujet, verbe_element, object_list)
                    sub_graph_sentence_list.append(sub_graph_sentence)
            else:
                sub_graph_sentence = SubGraphSentence(None, verbe_element, object_list)
                sub_graph_sentence_list.append(sub_graph_sentence)
        return sub_graph_sentence_list

    def subjects_extract(self, verbe_element, subject_patterns):
        result_subjects=[]
        subject=[]
        subject_element_origin = self.find_position_subject(verbe_element)
        if subject_element_origin is None:
            return []
        subjects_element_list = self.get_subjets_chunk_by_id(subject_element_origin)
        subject_length = len(subjects_element_list)
        #create the motif NC_ADJ
        for subject_elements in subjects_element_list:
            pos_tag_subject=""
            for element in subject_elements:
                pos_tag_subject = pos_tag_subject + element.postag +"_"
            pos_tag_subject = pos_tag_subject.strip("_").replace("+","P")
            #use lemma and compare with pattern
            list_position = self.find_the_best_pattern(subject_patterns,pos_tag_subject)
            if len(list_position)!=0:
                for position in list_position:
                    part1, part2, part2="","",""
                    part1 = pos_tag_subject[0:position[0]].strip("_")
                    part2 = pos_tag_subject[position[0]:position[1]]
                    #if position[1]<len(str):
                    #   part3 = pos_tag_sentence[position[1]+1:len(str)].strip("_")
                    term=""
                    term_lemma=""
                    start = len(self.str_list_remove_null(part1.split("_")))
                    end = start + len(self.str_list_remove_null(part2.split("_")))
                    for i in range(start, end):
                        subject.append(subject_elements[i])
                        #term = term +" " +subject_elements[i].form
                        #term_lemma = term_lemma + " "+ subject_elements[i].lemma
                    #term = term.strip(" ")
                    #term_lemma = term_lemma.strip(" ")
                    result_subjects.append(subject)
                    subject=[]
        return result_subjects

    def find_position_subject(self, verbe_element):
        subject_element = None
        abc=""
        for word_element in self.sentence.words():
            abc=abc+ word_element.postag +"_"
            if word_element.deprel == 'suj' and word_element.head <= verbe_element.id:
                subject_element = word_element
        print abc
        return subject_element

    def verbe_extract(self):
        verbe_element=None
        for word_element in self.sentence.words():
            if word_element.deprel == 'root' and word_element.postag == 'V':
                verbe_element = word_element
        return verbe_element


    def object_extract(self, verbe_element, object_patterns):
        result_objects = []
        objects = []
        object_element_origin = self.find_position_object(verbe_element)
        if object_element_origin is None:
            return []
        object_element_list = self.get_objects_chunk_by_id(object_element_origin)
        object_length = len(object_element_list)
        # create the motif NC_ADJ
        for object_elements in object_element_list:
            pos_tag_object = ""
            for element in object_elements:
                pos_tag_object = pos_tag_object + element.postag + "_"
            pos_tag_object = pos_tag_object.strip("_").replace("+","P")

            # use lemma and compare with pattern
            list_position = self.find_the_best_pattern(object_patterns, pos_tag_object)
            if len(list_position) != 0:
                for position in list_position:

                    part1, part2, part2 = "", "", ""
                    part1 = pos_tag_object[0:position[0]].strip("_")
                    part2 = pos_tag_object[position[0]:position[1]]
                    # if position[1]<len(str):
                    #   part3 = pos_tag_sentence[position[1]+1:len(str)].strip("_")
                    term = ""
                    term_lemma = ""
                    start = len(self.str_list_remove_null(part1.split("_")))
                    end = start + len(self.str_list_remove_null(part2.split("_")))
                    print start, end
                    for i in range(start, end):
                        print object_elements[i].form
                        objects.append(object_elements[i])
                        # term = term +" " +subject_elements[i].form
                        # term_lemma = term_lemma + " "+ subject_elements[i].lemma
                    # term = term.strip(" ")
                    # term_lemma = term_lemma.strip(" ")
                    result_objects.append(objects)
                    objects=[]
        return result_objects

    def find_position_object(self, verbe_element):
        object_element = None
        abc=""
        for word_element in self.sentence.words():
            abc=abc+ word_element.postag +"_"
            if word_element.deprel == 'obj' and word_element.head >= verbe_element.id:
                return word_element
        print abc
        return object_element

    def get_objects_chunk_by_id (self, object_element):
        id=int(object_element.id)
        object_element_list=[]
        sublist =[]
        while id != 0 and self.sentence.words()[id].postag != "PONCT":
            sublist.append(self.sentence.words()[id])
            if self.sentence.words()[id].cpostag == "CC":
                object_element_list.append(sublist)
                sublist=[]
            id=id-1

        object_element_list.append(sublist)
        return object_element_list

    def a_object_extract(self):
        a_object = ""
        return a_object

    def p_object_extract(self):
        p_object=""

    def de_object_extract(self):
        de_object=""
    #get the subject in the sentence
    def get_subjets_chunk_by_id (self, subject_element):
        id=int(subject_element.id)
        subject_element_list=[]
        sublist =[]
        while id != 0 and self.sentence.words()[id].postag != "PONCT":
            sublist.append(self.sentence.words()[id])
            if self.sentence.words()[id].cpostag == "CC":
                subject_element_list.append(self.reverse_array(sublist))
                sublist=[]
            id=id-1
        news_array = []
        subject_element_list.append(self.reverse_array(sublist))
        return subject_element_list

    def get_position_match_with_pattern(self, regex, pos_tag_sentence):
        # >>> pattern ="NN_NN+"
        # str="NN_NN_NN_CD_NN_NN_DD_NN"
        # [(m.start(0), m.end(0)) for m in re.finditer(pattern, str)]
        # [(0, 5), (12, 17)]
        return [(m.start(0), m.end(0)) for m in re.finditer(regex, pos_tag_sentence)]

    def str_list_remove_null(self, str_list):
        while ('' in str_list):
            str_list.remove('')
        return str_list

    def find_the_best_pattern(self, subject_patterns,pos_tag_subject):
        result = []
        distance_min =1000
        for patterm_candidate in subject_patterns:
            distance = abs(len(pos_tag_subject.split())-len(patterm_candidate.split()))
            list_position = self.get_position_match_with_pattern(patterm_candidate,pos_tag_subject)
            if len(list_position)!=0  and distance<=distance_min:
                result = list_position
                distance_min = distance
        return result


    def sort_array(self,news_aray,type="asc"):
        if type!="asc":
           array = news_aray.sort(key=lambda x: len(x.split("_")))
        else:
            array = reversed(news_aray.sort(key=lambda x: len(x.split("_"))))
        return array

    def reverse_array(self,array):
        news_array=[]
        item = len(array)-1
        while item >=0:
            news_array.append(array[item])
            item = item -1
        return news_array

