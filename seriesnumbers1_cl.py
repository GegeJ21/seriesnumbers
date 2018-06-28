
from PySide import QtGui
from seriesnumbers import guiControls
import sys


def main():
    my_app = QtGui.QApplication(sys.argv)
    ex = guiControls.Series_UI()
    ex.show()

    sys.exit(my_app.exec_())


if __name__ =='__main__':
    main()
