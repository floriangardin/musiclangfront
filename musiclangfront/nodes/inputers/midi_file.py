from musiclang import Score

from NodeGraphQt import NodeGraph
from ..base import AsyncProcessingNode

class MidiFileNode(AsyncProcessingNode):
    """
    Convert a midi file to a musiclang score.
    """

    # unique node identifier.
    __identifier__ = 'inputer'

    # initial default node name.
    NODE_NAME = 'MidiFile'

    def __init__(self):
        super(MidiFileNode, self).__init__()
        # create input & output ports
        self.add_output('score')
        # create QLineEdit text input widget.
        self.create_property('score', None)
        self.add_text_input('path', 'Relative path :', tab='widgets')
        self.add_button('load', '', 'Load File')
        self.get_widget('load').get_custom_widget().clicked.connect(self.execute)

    def compute(self):
        # Update from
        import os
        score = None
        path = self.get_property('path')
        try:
            score = Score.from_midi(os.path.join(NodeGraph.PROJECT_PATH, path))
        except Exception as e:
            print(e)
            pass
        self.set_property('score', score)
