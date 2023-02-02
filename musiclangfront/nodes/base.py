from NodeGraphQt import BaseNode


class ProcessingNode(BaseNode):
    """
        An example of a node passing values automatically
        """

    # unique node identifier.
    __identifier__ = 'nodes.processing'

    # initial default node name.
    NODE_NAME = 'processing'


    @classmethod
    def from_function(cls, fn):
        from pdb import set_trace; set_trace()
        pass


    def __init__(self):
        super(ProcessingNode, self).__init__()
        self.children = {}

    def add_child(self, name, node):
        self.children[name] = node

    def remove_child(self, name):
        del self.children[name]

    def compute(self):
        """
        Override this method if you want a specific computation for the node

        """
        pass

    def on_input_connected(self, in_port, out_port):
        """
        Callback triggered when a new pipe connection is made.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_disconnected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that connected to this node.
        """
        out_port.node().add_child((out_port.name(), in_port.name()), in_port.node())
        out_port.node().execute()
        return

    def on_input_disconnected(self, in_port, out_port):
        """
        Callback triggered when a pipe connection has been disconnected
        from a INPUT port.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_connected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that was disconnected.
        """
        out_port.node().remove_child((out_port.name(), in_port.name()))
        return

    def execute(self, *args, **kwargs):
        self.compute()
        for key, child_node in self.children.items():
            out_name, in_name = key
            child_node.set_property(in_name, self.get_property(out_name))
            child_node.execute()


