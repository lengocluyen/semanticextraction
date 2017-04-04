import re

from SemanticExtraction.src.ATR.Annotation import Annotation

class TextBound(Annotation):
    """Textbound annotation representing entity mention or event trigger."""

    def __init__(self, id_, type_, spans, text):
        super(TextBound, self).__init__(id_,type_)
        if isinstance(spans, basestring):
            self.spans = TextBound.parse_spans(spans)
        else:
            self.spans = spans
        self.text = text

    def verify_text(self,text):
        offset = 0
        for start, end in self.spans:
            endoff = offset + (end - start)
            assert text[start:end] == self.text[offset:endoff], \
                'Error: text mismatch: "%s" vs. "%s"' % \
                (text[start:end], self.text[offset:endoff])
            offset = endoff + 1

    def __unicode__(self):
        span_str = u';'.join(u'%d %d' % (s[0], s[1]) for s in self.spans)
        return u'%s\t%s %s\t%s' % (self.id, self.type, span_str, self.text)

    @staticmethod
    def parse_spans(span_string):
        """Return list of (start, end) pairs for given span string."""
        spans = []
        for span in span_string.split(';'):
            start, end = span.split(' ')
            spans.append((int(start), int(end)))
        return spans