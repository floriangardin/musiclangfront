
from ..base import ProcessingNode
from musiclang.library import *

class TextToScoreNode(ProcessingNode):
    """
    An example of a node passing values automatically
    """

    # unique node identifier.
    __identifier__ = 'inputer'

    # initial default node name.
    NODE_NAME = 'Score'


    def __init__(self):
        super(TextToScoreNode, self).__init__()
        # create input & output ports
        self.add_output('score')
        # create QLineEdit text input widget.
        self.add_plain_text_input('text', 'Score :', tab='widgets')
        self.create_property('score', None)
        self.get_widget('text').value_changed.connect(lambda k, v: self.execute(k, v))

    def compute(self):
        # Update from
        score = None
        try:
            score = eval(str(self.get_property('text')).replace('\n', ''))
        except:
            print('Exception')
        self.set_property('score', score)
        pass



class TextToExpressionNode(ProcessingNode):
    """
    An example of a node passing values automatically
    """

    # unique node identifier.
    __identifier__ = 'inputer'

    # initial default node name.
    NODE_NAME = 'Expression'


    def __init__(self):
        super(TextToExpressionNode, self).__init__()
        # create input & output ports
        # create QLineEdit text input widget.
        self.add_text_input('text', 'Expression :', tab='widgets')
        self.get_widget('text').value_changed.connect(lambda k, v: self.execute(k, v))

        self.add_output('expr')
        self.create_property('expr', None)

    def compute(self):
        # Update from
        expr = None
        try:
            expr = eval(str(self.get_property('text')).replace('\n', ''))
        except:
            pass
        self.set_property('expr', expr)
        pass




