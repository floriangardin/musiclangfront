from NodeGraphQt import BaseNode
import threading

class ProcessingNode(BaseNode):
    """
    An example of a node passing values automatically
    """

    # unique node identifier.
    __identifier__ = 'nodes.processing'

    # initial default node name.
    NODE_NAME = 'processing'
    SEP = '|'

    @classmethod
    def from_function(cls, fn):
        from pdb import set_trace; set_trace()
        pass


    def __init__(self):
        super(ProcessingNode, self).__init__()
        self.create_property('children', {})

    @property
    def children(self):
        return self.get_property('children')

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
        # key = self.SEP.join([out_port.name(), in_port.name(), out_port.node().id, in_port.node().id])
        # out_port.node().add_child(key, in_port.node().id)
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
        return


    def execute_children(self):
        for key, port in self.outputs().items():
            children_ports = port.connected_ports()
            out_name = port.name()
            for child_port in children_ports:
                in_name = child_port.name()
                child_node = child_port.node()
                child_node.set_property(in_name, self.get_property(out_name))
                child_node.execute()

    def execute(self, *args, **kwargs):
        self.compute()
        self.execute_children()


class AsyncProcessingNode(ProcessingNode):

    def __init__(self):
        super(AsyncProcessingNode, self).__init__()
        self.add_checkbox('loading', '', 'is loading', state=False)
        self.loading_widget = self.get_widget('loading')
        self.loading_widget.value_changed.connect(lambda x: self.execute_children())

    def compute_async(self):
        self.loading_widget.set_value(True)
        self.compute()
        self.loading_widget.set_value(False)

    def execute(self, *args, **kwargs):
        x = threading.Thread(target=self.compute_async)
        x.start()

