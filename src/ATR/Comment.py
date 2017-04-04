import re
from SemanticExtraction.src.ATR.Annotation import Annotation

class Comment(Annotation):
    """Typed free-form text comment associated with another annotation."""

    def __init__(self, id_, type_, arg, text):
        super(Comment, self).__init__(id_, type_)
        self.arg = arg
        self.text = text

    def __unicode__(self):
        return '%s\t%s %s\t%s' % (self.id, self.type, self.arg, self.text)

    STANDOFF_RE = re.compile(r'^(\S+)\t(\S+) (\S+)\t(.*)$')