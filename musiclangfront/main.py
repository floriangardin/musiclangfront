#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget,
QFileSystemModel
)

from musiclangfront.nodes.library import ALL_NODES


# import example nodes from the "example_nodes" package
from musiclangfront import nodes

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry

        # calling method
        self.UiComponents()

        # showing all the widgets


    def init_graph_nodes(self, graph):

        graph.set_context_menu_from_file('./musiclangfront/hotkeys/hotkeys.json')
        graph.register_nodes(ALL_NODES)

        # create node with custom text color and disable it.
        n_score1 = graph.create_node(
            'inputer.TextToScoreNode', name='Score1', color='#0a1e20')

        n_score2 = graph.create_node(
            'inputer.TextToScoreNode', name='Score2', color='#0a1e20')

        midi_player = graph.create_node(
            'player.MidiPlayerNode', text_color='#feab20')

        merger = graph.create_node(
            'transformer.ConcatScoresNode', text_color='#feab20')


        n_score1.set_output(0, merger.input(0))
        n_score2.set_output(0, merger.input(1))
        merger.set_output(0, midi_player.input(0))

        # create a node properties bin widget.
        properties_bin = PropertiesBinWidget(node_graph=graph)
        properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # example show the node properties bin widget when a node is double clicked.
        def display_properties_bin(node):
            if not properties_bin.isVisible():
                properties_bin.show()

        # wire function to "node_double_clicked" signal.
        graph.node_double_clicked.connect(display_properties_bin)

    # method for widgets
    def UiComponents(self):

        graph = NodeGraph()
        # show the node graph widget.
        self.init_graph_nodes(graph)
        nodes_palette = NodesPaletteWidget(node_graph=graph)
        nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
        nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
        nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
        nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
        nodes_palette.set_category_label('nodes.group', 'Group Nodes')

        nodes_palette.resize(10, 100)

        model = QFileSystemModel(PROJECT_PATH)
        model.setRootPath()
        tree = QtWidgets.QTreeView()
        tree.setModel(model)
        tree.setAnimated(False)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)

        # adding border to label
        layout = QtWidgets.QGridLayout()
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)
        layout.addWidget(tree, 0, 0, 12, 2)
        layout.addWidget(graph.widget, 0, 2, 12, 8)
        layout.addWidget(nodes_palette, 0, 10, 12, 2)



        self.setLayout(layout)
        # opening window in maximized size
        self.showMaximized()

        graph.auto_layout_nodes()
        graph.clear_selection()
        graph.fit_to_selection()


if __name__ == '__main__':

    #play_music()
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])
    window = Window()

    app.exec_()
