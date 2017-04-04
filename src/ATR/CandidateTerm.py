
class CandidateTerm(object):

    def __init__(self, term, term_lemma, wordnet, frequence,  subfrequence =0 , cvalue=0,other=None, subterms=[], supterms=[]):
        self.term = term
        self.term_lemma = term_lemma

        self.wordnet = wordnet
        self.frequence = frequence
        self.subfrequence = subfrequence
        self.subterms = subterms
        self.supterms = supterms
        self.cvalue = cvalue
        self.other = other


    def __unicode__(self):
        fields = [self.term, self.term_lemma, self.wordnet, self.frequence, self.subfrequence, self.cvalue,self.other]
        return "\t".join(fields)