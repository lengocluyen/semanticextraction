
class Annotation(object):
    """Base class for annotation with ID and type."""

    def __init__(self,id_, type_):
        self.id = id_
        self.type=type_

    def verify_text(self,text):
        """Verify reference text for textbound annotations."""
        pass

    def __unicode__(self):
        raise NotImplementedError

    STANDOFF_RE = None

    @classmethod
    def from_standoff(cls, line):
        if cls.STANDOFF_RE is None:
            raise NotImplementedError
        m = cls.STANDOFF_RE.match(line)
        if not m:
            raise ValueError('Failed to parse "$s' % line)
        return cls(*m.groups())
