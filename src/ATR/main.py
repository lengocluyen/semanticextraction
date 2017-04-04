import json
import os
import sys

import xmltodict

from SemanticExtraction.src.ATR.CandidateTermExtraction import CandidateTermExtraction
from SemanticExtraction.src.ATR.CoNLLXHandle import CoNLLXHandle
from SemanticExtraction.src.ATR.FormatError import FormatError
from SemanticExtraction.src.ATR.TripleExtraction import  TripleExtraction
from SemanticExtraction.src.ATR.GraphExtraction.SubGraphControl import SubGraphControl


def convert_xml_to_json():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    '''xml_file_path ="/home/lengocluyen/Data/wonef12.xml"
    json_output = "/home/lengocluyen/Data/wonef12.json"
    xml_file = open(xml_file_path,"r")

    xml_content = xmltodict.parse(xml_file)
    json_data = json.dumps(xml_content)
    file =  open(json_output,"w")
    file.write(json_data)
    xml_file.close()
    file.close()'''

    xml_file_path = "/home/lengocluyen/Data/Wonef"
    json_output = "/home/lengocluyen/Data/Wonef_JSON"

    for name in os.listdir(xml_file_path):
        path = os.path.join(xml_file_path, name)

        if os.path.isfile(path) and not name.startswith('.'):
            xml_file = open(path, "r")
            xml_content = xmltodict.parse(xml_file)
            json_data = json.dumps(xml_content)
            json_save = os.path.join(json_output, name +".json")
            print "saving ... " + json_save
            file = open(json_save, "w")
            file.write(json_data)
            xml_file.close()
            file.close()


def extract_termes():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    dir = "/home/lengocluyen/Data/sample/outmap/"
    output="/home/lengocluyen/Data/sample/terms2.txt"
    candidate_term_list=[]
    stopwords_path  ="/home/lengocluyen/Data/french.stoplist.txt"
    stopwords = [line.rstrip('\n') for line in open(stopwords_path)]
    for i in stopwords:
        print i
    pattern = [
               #"NC_",
                "NC_ADJ",
                "NC_ADJ_ADJ",

                "NC_PPD_NC",
                "NC_PPD_NC_ADJ",
               "NC_ADJ_PPD_NC",
                "NC_ADJ_PPD_NC_ADJ",

               "NC_P_PPD_NC",
                "NC_P_PPD_NC_ADJ",
                "NC_ADJ_P_PPD_NC",
                "NC_ADJ_P_PPD_NC_ADJ",

                "NC_P_DET_NC",
                "NC_ADJ_P_DET_NC",
                "NC_P_DET_NC_ADJ",
                "NC_ADJ_P_+DET_NC_ADJ",

                "NC_P_DET_NC_P_DET_NC_ADJ",
                "NC_P_DET_NC_ADJ_P_DET_NC_ADJ",
                "NC_ADJ_P_DET_NC_ADJ_P_DET_NC_ADJ",
                "NC_ADJ_P_DET_NC_ADJ_P_DET_NC",
                "NC_P_DET_NC_ADJ_P_DET_NC_ADJ",
               "NC_ADJ_P_DET_NC_P_DET_NC_ADJ",

                "NC_NPP_P_DET_NC_ADJ",
                #"NC_NPP",
                "NC_P_DET_NC",
                "NC_P_NC",
                "NC_ADJ_NC",
                "NC_PPD_NC_ADJ_NC",
                "NC_PPD_NC", "NC_ADJ_P_NC_NC",
                "NC_ADJ_P_NC_P_NC","NC_PREF_NC_ADJ",
                "NC_PPD_NC_PREF_NC", "NC_PPD_NC_PREF_NC_ADJ",
                "NC_P_DET_NC", "NC_P_NC_PPD_NC_ADJ"


                ]

    candidate_term = CandidateTermExtraction(candidate_term_list,stopwords,dir,pattern)
    candidate_term.get_all_term_from_all_file_corpus()
    candidate_term.to_string(output)

def extract_triple():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    dir = "/home/lengocluyen/Data/sample/outmap/"
    term_list = "/home/lengocluyen/Data/sample/terms.txt"
    triple_output="/home/lengocluyen/Data/sample/triples.txt"
    candidate_triple_list = []
    stoptriple_path = "/home/lengocluyen/Data/french.stoplist.txt"
    stoptriple = [line.rstrip('\n') for line in open(stoptriple_path)]

    pattern = {
                  "NC_V_VINF_P_DET_NC_PPD_NC_NPP_P_NC_P_DET_NC_ADJ":"NC:V_VINF_P:DET_NC__PPD_NC_NPP_P_NC_P_DET_NC_ADJ",
              "NC_ADJ_V_VINF_ADJ_PPD_NC_P_NC":"NC_ADJ:V_VINF_ADJ_PPD:NC_P_NC",
                "NC_PPD_NC_NPP_V_VPP_DET_ADJ_NC_P_DET_NC":"NC_PPD_NC_NPP:V_VPP:DET_ADJ_NC_P_DET_NC",
            "NC_V_VPP_PPD_NC":"NC:V_VPP:PPD_NC",
        "NC_NC_VPP_P_DET_NC":"NC_NC:VPP_P:DET_NC",

        "CLS_V_DET_NC":"CLS:V:DET_NC",
        "CLS_V_P_NC":"CLS:V_P:NC",
        "CLS_V_P_DET_NC":"CLS:V_P:DET_NC",
        "CLS_V_P_VINF_DET_NC":"CLS:V_P_VINF:DET_NC",
        "CLO_VINF_P_DET_NC":"CLO:VINF_P:DET_NC",
        "CLS_V_VINF_VPP_P_DET_NC":"CLS:V_VINF_VPP_P:DET_NC",
        "NC_NPP_V_VPP_P_DET_NC":"NC_NPP:V_VPP_P:DET_NC",
        "NC_V_VPP_ADJ_P_NC":"NC:V_VPP_ADJ_P:NC",
        "NC_V_VPP_P_DET_NC":"NC:V_VPP_P:DET_NC",

        "NC_V_CLS_V_P_PRO":"NC:V_CLS_V_P:PRO",
        "NC_P_DET_NC_P_NC_V_P_VINF_DET_NC":"NC_P_DET_NC_P_NC:V_P_VINF:DET_NC",
        "CLS_V_ADV_DET_NC":"CLS:V_ADV:DET_NC",
                           "CLS_V_ADV_DET_NC_P_NC_P_NC":"CLS:V_ADV:DET_NC_P_NC_P_NC"
            }


    #self, triple_list, term, stoptriples, corpus_path, pattern):
    triple_list=[]
    #for word in [line.rstrip('\n') for line in open(term_list)]:
     #   term = word.split("\t")[0]
    triple_extraction = TripleExtraction(triple_list,stoptriple, dir, pattern)
    triple_extraction.get_all_triple_from_all_file_corpus()
    triple_extraction.to_string_and_file(triple_output)

def extract_sub_graph():
    path_subject_pattern = "../../sample/subject_pattern.txt"
    path_outmat = "/home/lengocluyen/Data/sample/outmap/"
    path_output_filename="../../sample/output/sub_graph_extract.txt"
    sub_graph_control = SubGraphControl(path_outmat,path_subject_pattern)
    sub_graph_sentence_list = sub_graph_control.extract_sub_graph_in_sentence()
    sub_graph_control.to_string(path_output_filename,sub_graph_sentence_list)

def createTree():
    # process sentence at a time

    conllx = CoNLLXHandle()
    #dir = "/home/lengocluyen/Data/output/"
    #inputdir = "/home/lengocluyen/Data/txt/"

    dir = "/home/lengocluyen/Data/sample/output/"
    inputdir = "/home/lengocluyen/Data/sample/outmap/"

    list = []
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            i=0
            for sentence in conllx.read_conllx(f):
                sent_count += 1
                word_count += len(sentence.words())

                print sentence.to_normal_sentence()
                print "\n"

                dotgraph = sentence.as_dotgraph()
                print dotgraph
                name = str(dir) + str(i) + '_'+ sentence.words()[0].lemma
                #print name
                dotgraph.render(name)
                i=i+1

                #for element in sentence.words():
                 #   print element.form

            print '%s: %d sentences, %d words' % (f, sent_count, word_count)

        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))

    # process document at a time
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            for document in conllx.read_documents(f):
                sent_count += len(document.sentences())
                word_count += len(document.words())
            print '%s: %d sentences, %d words' % (f, sent_count, word_count)
        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))


if __name__ == '__main__':
    sys.exit(extract_sub_graph())
    #sys.exit(extract_triple())
    #sys.exit(main(sys.argv))
    #sys.exit(main())
    #sys.exit(createTree())
    #sys.exit(extract_termes())
    #sys.exit(convert_xml_to_json())