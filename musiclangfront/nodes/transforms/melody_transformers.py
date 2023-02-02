from ..base import ProcessingNode

class ReverseMelodyNode(ProcessingNode):
    """
    An example of a node passing values automatically
    """

    # unique node identifier.
    __identifier__ = 'transformer'

    # initial default node name.
    NODE_NAME = 'ReverseMelody'


    def __init__(self):
        super(ReverseMelodyNode, self).__init__()
        # create input & output ports
        # create QLineEdit text input widget.
        self.create_property('data', None)
        # create input and output port.
        self.add_input('data')
        self.add_output('score')
        self.create_property('score', None)

    def compute(self):
        score = None
        try:
            from musiclang.transform.library import ReverseMelody
            score = ReverseMelody()(self.get_property('data'))
        except:
            pass
        self.set_property('score', score)
        pass


