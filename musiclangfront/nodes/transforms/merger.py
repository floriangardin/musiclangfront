from ..base import ProcessingNode

class ConcatScoresNode(ProcessingNode):
    """
    An example of a node passing values automatically
    """

    # unique node identifier.
    __identifier__ = 'transformer'

    # initial default node name.
    NODE_NAME = 'ConcatScores'


    def __init__(self):
        super(ConcatScoresNode, self).__init__()
        # create input & output ports
        # create QLineEdit text input widget.
        self.create_property('data', None)
        # create input and output port.
        self.n = 2

        self.add_integer_input('nb', 'Number of inputs :', value=self.n, tab='widgets')

        self.create_property('i0', None)
        self.add_input('i0')
        self.create_property('i1', None)
        self.add_input('i1')

        self.add_output('score')

        self.set_port_deletion_allowed(True)
        self.get_widget('nb').value_changed.connect(lambda k, v: self.add_or_remove(k, v))

        self.create_property('score', None)

    def add_or_remove(self, k, value):
        if self.n > value:
            for i in range(value, self.n):
                # Delete ports
                self.get_input(f'i{i}').clear_connections()
                # Delete inputs
                self.delete_input(f'i{i}')
        elif self.n < value:
            for i in range(self.n, value):
                self.add_input(f'i{i}')
                if self.has_property(f'i{i}'):
                    self.set_property(f'i{i}', None)
                else:
                    self.create_property(f'i{i}', None)

        self.n = value
        self.execute()


    def on_input_disconnected(self, in_port, out_port):
        super(ConcatScoresNode, self).on_input_disconnected(in_port, out_port)
        in_port.node().set_property(in_port.name(), None)
        self.execute()

    def compute(self):
        from musiclang.transform.library import ConcatScores
        score = None
        result = [self.get_property(f'i{i}') for i in range(self.n)]
        try:
            score = ConcatScores()(*result)
        except:
            pass
        self.set_property('score', score)
        pass


