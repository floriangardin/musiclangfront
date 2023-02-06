from Qt import QtWidgets


class FileTreeViewer(QtWidgets.QTreeView):

    # constructor
    def __init__(self, parent=None):
        super(FileTreeViewer, self).__init__(parent)

        # overriding the mouseDoubleClickEvent method
    def mouseDoubleClickEvent(self, event):
        print(event.__dir__())
        print("Mouse Double Click Event", event)