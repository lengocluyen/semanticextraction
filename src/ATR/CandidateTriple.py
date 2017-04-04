
class CandidateTriple(object):
    def __init__(self,subject, verb, object, subject_lemma, verb_lemma, object_lemma):
        self.subject = subject
        self.verb  = verb
        self.object = object
        self.subject_lemma = subject_lemma
        self.verb_lemma = verb_lemma
        self.object_lemma = object_lemma

    def to_string(self):
        return "(" + self.subject +", " +self.verb + ", " + self.object + ") - lemma - (" + self.subject_lemma +", " +self.verb_lemma + ", " + self.object_lemma + ")"