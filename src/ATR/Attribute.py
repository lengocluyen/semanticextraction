import re
from SemanticExtraction.src.ATR.Annotation import Annotation

class Attribute(Annotation):
    """Attribute with optional value associated with another annotation."""

    def __init__(self, id_, type_, arg, val):
        super(Attribute, self).__init__(id_, type_)
        self.arg = arg
        self.val = val

    def __unicode__(self):
        if not self.val:
            return '%s\t%s %s' % (self.id, self.type, self.arg)
        else:
            return '%s\t%s %s %s' % (self.id, self.type, self.arg, self.val)

    STANDOFF_RE = re.compile(r'^(\S+)\t(\S+) (\S+) ?(\S*)$')