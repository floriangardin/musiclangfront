#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal

from Qt import QtCore, QtWidgets
import Qt

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget,
)
from PyQt5.QtWidgets import (
    QWidget,
    QFileSystemModel
)


## LOAD NECESSARY LIBRARIES
from musiclangfront.nodes.library import ALL_NODES
from musiclangfront.midi_player.score_to_midi import MidiPlayer
from musiclangfront import nodes
from musiclang.analyze.augmented_net.inference import get_model

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
EXAMPLE_PATH = os.path.join(PROJECT_PATH, "locals/example")

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("MusicLang")

        self.tree = None
        self.tab_widget = None
        self.layout = None
        self.graphs = {}

        self.graph_container = None
        self.nodes_palette_container = None
        self.curr_graph_idx = None
        self.tabs_idx = []
        # setting geometry

        # calling method
        self.UiComponents()
        # showing all the widgets


    def init_graph_nodes(self, graph):



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


    def addTab(self, filename):
        tab_idx = self.tab_widget.addTab(filename)
        self.tabs_idx.append(tab_idx)
        return tab_idx

    def openNewGraph(self, filepath=None):


        if filepath is None:
            import tempfile
            with tempfile.NamedTemporaryFile() as f:
                return self.openNewGraph(f.name)


        if filepath == self.curr_graph_idx:
            return

        if filepath in self.graphs.keys():
            ## Just show these
            graph, nodes_palette, tab_idx = self.graphs[filepath]
            graph.widget.show()
            nodes_palette.show()
        else:
            graph = NodeGraph()
            file_loaded = os.path.join(filepath)
            filename = os.path.basename(file_loaded)
            graph.set_project_path(EXAMPLE_PATH)
            graph.set_context_menu_from_file('./musiclangfront/hotkeys/hotkeys.json')
            graph.register_nodes(ALL_NODES)
            graph.load_session(file_loaded)

            tab_idx = self.addTab(filename)

            nodes_palette = NodesPaletteWidget(node_graph=graph)
            nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
            nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
            nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
            nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
            nodes_palette.set_category_label('nodes.group', 'Group Nodes')
            nodes_palette.resize(10, 100)
            graph.auto_layout_nodes()
            graph.clear_selection()
            graph.fit_to_selection()
            self.graphs[filepath] = (graph, nodes_palette, tab_idx)
            self.graphs[tab_idx] = (graph, nodes_palette, filepath)

        self.tab_widget.setCurrentIndex(tab_idx)
        self.reconstructLayout(graph, nodes_palette)

        self.curr_graph_idx = filepath


    def removeCurrentTabFromLayout(self, graph_widget, nodes_palette):
        self.graph_container.removeWidget(graph_widget)
        self.graph_container.removeWidget(graph_widget)
        self.nodes_palette_container.removeWidget(nodes_palette)

    def reconstructLayout(self, graph=None, nodes_palette=None):
        # adding border to label

        if graph is not None:
            if self.curr_graph_idx in self.graphs.keys():
                old_graph, old_node_palette, old_tab_idx = self.graphs[self.curr_graph_idx]
                self.graph_container.replaceWidget(old_graph.widget, graph.widget)
                old_graph.widget.hide()
                self.nodes_palette_container.replaceWidget(old_node_palette, nodes_palette)
                old_node_palette.hide()
            else:
                self.graph_container.addWidget(graph.widget)
                self.nodes_palette_container.addWidget(nodes_palette)



    def initLayout(self):
        # adding border to label
        self.layout = QtWidgets.QGridLayout()
        self.layout.setHorizontalSpacing(12)
        self.layout.setVerticalSpacing(24)
        self.layout.addWidget(self.tree, 0, 0, 24, 2)
        tab_with_layout = QtWidgets.QHBoxLayout()
        tab_with_layout.addWidget(self.tab_widget)
        tab_with_layout.addStretch()
        self.layout.addLayout(tab_with_layout, 0, 2, 1, 8)

        # Set graph and node palette container
        self.graph_container = QtWidgets.QHBoxLayout()
        self.nodes_palette_container = QtWidgets.QHBoxLayout()

        self.layout.addLayout(self.graph_container, 1, 2, 23, 8)
        self.layout.addLayout(self.nodes_palette_container, 0, 10, 24, 2)


    def clickOnTab(self, tab_idx):
        # Get graph
        graph, nodes_palette, filepath = self.graphs[tab_idx]
        self.openNewGraph(filepath)


    def removeAndAssignNewTabIdx(self, tab_idx):
        # Assign new tab
        tab_idx_index = self.tabs_idx.index(tab_idx)
        print(self.tabs_idx, tab_idx, tab_idx_index)
        print(self.graphs.keys())
        self.tabs_idx.remove(tab_idx)

        if len(self.tabs_idx) > 0:
            if tab_idx_index > 0:
                self.clickOnTab(self.tabs_idx[tab_idx_index - 1])
            else:
                print(tab_idx_index, self.tabs_idx)
                self.clickOnTab(self.tabs_idx[tab_idx_index])


    def removeTab(self, tab_idx_index):
        tab_idx = self.tabs_idx[tab_idx_index]
        self.tab_widget.removeTab(tab_idx_index)
        graph, nodes_palette, filepath = self.graphs[tab_idx]
        del self.graphs[filepath]
        del self.graphs[tab_idx]
        assert filepath not in self.graphs
        # If it was current tab, remove from layout
        if self.curr_graph_idx == filepath:
            self.removeCurrentTabFromLayout(graph.widget, nodes_palette)
            self.curr_graph_idx = None
        graph.widget.deleteLater()
        nodes_palette.deleteLater()
        self.removeAndAssignNewTabIdx(tab_idx)

    # method for widgets
    def UiComponents(self):

        self.tab_widget = QtWidgets.QTabBar()
        self.tab_widget.setMovable(True)
        self.tab_widget.setExpanding(False)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.removeTab)
        self.tab_widget.tabBarClicked.connect(self.clickOnTab)

        # show the node graph widget.
        #self.init_graph_nodes(graph)

        model = QFileSystemModel()
        model.setRootPath(EXAMPLE_PATH)
        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(model)
        self.tree.setRootIndex(model.index(EXAMPLE_PATH))
        self.tree.setAnimated(False)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.doubleClicked.connect(lambda x: self.openNewGraph(x.model().filePath(x)))


        self.initLayout()
        self.setLayout(self.layout)
        self.showMaximized()

        self.openNewGraph()




if __name__ == '__main__':

    #play_music()
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])
    window = Window()

    app.exec_()
