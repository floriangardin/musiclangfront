from ..base import ProcessingNode
from Qt import QtCore, QtWidgets

class MidiPlayerNode(ProcessingNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'player'

    # set the initial default node name.
    NODE_NAME = 'MidiPlayer'


    def __init__(self):
        from musiclangfront.midi_player import MidiPlayer
        super(MidiPlayerNode, self).__init__()
        self.btn_play = QtWidgets.QPushButton('Go')
        # create the checkboxes.
        self.add_button('button_play', '', 'Play')
        self.add_button('button_stop', '', 'Stop')
        self.get_widget('button_play').get_custom_widget().clicked.connect(self.play)
        self.get_widget('button_stop').get_custom_widget().clicked.connect(self.stop)
        self.create_property('data', None)
        # create input and output port.
        self.add_input('data')
        self.midi_player = MidiPlayer()


    def stop(self):
        self.midi_player.stop_music()

    def play(self):
        value = self.get_property('data')
        self.midi_player.play_score(value)

    def compute(self):
        pass

