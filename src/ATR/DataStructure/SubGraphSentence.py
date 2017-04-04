
'''
Data strucutre for extracting the sub graph in sentence
for example, there is a sentence: "Gerald aime Alice et Beatrice"
[V < suj[N] < coord[P < obj[N] < obj[N]]]
'''
class SubGraphSentence(object):
    def __init__(self, subject, verb, objects):
        self.subject = subject
        self.verb = verb
        self.objects = objects

    def convert_element_to_string(sell, element_list):
        result = ""
        for element in element_list:
            result = result + element.form + " "
        return result.strip(" ")

    def to_string(self):
#        for i in range(0,len(self.objects)-2):
 #           object_list +=  self.objects[i] + "<"
  #      object_list += self.objects[len(self.objects)-2]
        if len(self.objects)>1:
            verb_string = self.verb.lemma
            if self.subject is not None:
                subject_string = self.convert_element_to_string(self.subject)
            else:
                subject_string =""
            object_list_string =""
            for object_elements in self.objects:
                object_list_string += self.convert_element_to_string(object_elements) + ", "
            object_list_string =  object_list_string.rstrip(", ")
            return "[" + verb_string + " < " + subject_string + "< coord [" + object_list_string + "]"
        else:
            verb_string = self.verb.lemma
            if self.subject is not None:
                subject_string = self.convert_element_to_string(self.subject)
            else:
                subject_string =""
            object_list_string=""
            for object_elements in self.objects:
                object_list_string =object_list_string + self.convert_element_to_string(object_elements)+ ", "
            object_list_string =  object_list_string.rstrip(", ")
            return "["+verb_string+" < "+ subject_string + " < " + object_list_string+"]"

