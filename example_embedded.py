import sys
from PySide import QtGui

from ui_embedded_example import Ui_MainWindow

class ApplicationWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        # Ui_MainWindow method
        self.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
