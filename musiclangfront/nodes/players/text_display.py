from ..base import ProcessingNode
from Qt import QtCore, QtWidgets
from musiclangfront.midi_player import MidiPlayer


class ScoreDisplayerNode(ProcessingNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'player'

    # set the initial default node name.
    NODE_NAME = 'ScoreDisplayer'


    def __init__(self):
        super(ScoreDisplayerNode, self).__init__()
        self.btn_play = QtWidgets.QPushButton('Go')
        # create the checkboxes.
        self.add_plain_text_input('data', 'Score :', '')
        # create input and output port.
        self.add_input('score')
        self.create_property('score', None)

    def compute(self):
        text = str(self.get_property('score'))
        self.get_widget('data').set_value(text)

