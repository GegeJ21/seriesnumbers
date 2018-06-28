from PySide import QtGui
from PySide import QtCore
import sys, os
import fibonacci, padovan
import myColorPicker
import output

FIBONACCI_STRING = "Fibonacci"
PADOVAN_STRING = "Padovan"
# path to the icons folder
PATH_TO_ICONS = os.path.join(os.path.dirname(__file__), "icons")
# absolute path of the icons
SHELL_ICON = os.path.join(PATH_TO_ICONS, "shell.png")
SUM_ICON = os.path.join(PATH_TO_ICONS, "sum.png")
PLAY_ICON = os.path.join(PATH_TO_ICONS, "play.png")
STOP_ICON = os.path.join(PATH_TO_ICONS, "stop.png")
COLOR_ICON = os.path.join(PATH_TO_ICONS, "color.png")
FILE_FILTERS = "Text(.txt);;Jason(.json);;Exel(.csv)"

class Series_UI(QtGui.QWidget):

    def __init__(self):

        super(Series_UI, self).__init__()

        self.setGeometry(200,200,400,500)

        total_layout = QtGui.QVBoxLayout()
        
        # layout of the series picker and the parameters spin boxes
        top_layout = QtGui.QHBoxLayout()

        self.__series_picker = QtGui.QComboBox() 
        self.__series_picker.addItem(FIBONACCI_STRING)
        self.__series_picker.addItem(PADOVAN_STRING)

        options_layout = QtGui.QFormLayout()

        self.__recursion_spinner = QtGui.QDoubleSpinBox()
        self.__recursion_spinner.setRange(1, 1000)
        self.__recursion_spinner.setDecimals(0)
        options_layout.addRow("Recursions", self.__recursion_spinner)

        self.__offset_spinner = QtGui.QDoubleSpinBox()
        self.__offset_spinner.setRange(0, 100)
        self.__offset_spinner.setDecimals(0)
        options_layout.addRow("Offset", self.__offset_spinner)

        self.__multiply_spinner = QtGui.QDoubleSpinBox()
        self.__multiply_spinner.setRange(1, 100)
        self.__multiply_spinner.setDecimals(0)
        options_layout.addRow("Multiply", self.__multiply_spinner)

        top_layout.addWidget(self.__series_picker)
        top_layout.addLayout(options_layout)
        
        # layout of start end stop buttons
        run_layout = QtGui.QHBoxLayout()
        run_layout.addSpacing(50)

        self.__generate_button = QtGui.QPushButton(self)
        self.__generate_button.setIcon(QtGui.QIcon(PLAY_ICON))
        self.__generate_button.clicked.connect(self.startGenereteSeries)
        run_layout.addWidget(self.__generate_button)

        run_layout.addSpacing(10)

        self.__stop_button = QtGui.QPushButton(self)
        self.__stop_button.setIcon(QtGui.QIcon(STOP_ICON))
        self.__stop_button.setEnabled(False)
        run_layout.addWidget(self.__stop_button)

        run_layout.addSpacing(50)

        # layout for the Turtle Graphics options
        turtle_layout = QtGui.QHBoxLayout()
        turtle_layout.addSpacing(50)

        self.__turtle_runner = QtGui.QPushButton(self)
        self.__turtle_runner.clicked.connect(self.displayTurtle)
        self.__turtle_runner.setEnabled(False)
        self.__turtle_runner.setIcon(QtGui.QIcon(SHELL_ICON))
        turtle_layout.addWidget(self.__turtle_runner)
        turtle_layout.addSpacing(10)

        self.__color_button = QtGui.QPushButton()
        self.__color_button.setIcon(QtGui.QIcon(COLOR_ICON))
        self.__color_button.clicked.connect(self.openColorPicker)
        self.__color_picker = myColorPicker.MyColorPickerDialog()
        turtle_layout.addWidget(self.__color_button)
        turtle_layout.addSpacing(50)

        self.__progress_bar = QtGui.QProgressBar()
        self.__progress_bar.setAlignment(QtCore.Qt.AlignHCenter)
        self.__progress_bar.setValue(0)

        self.__result_list = QtGui.QListWidget()

        self.__export_button = QtGui.QPushButton("Export")
        self.__export_button.clicked.connect(self.openFileDialog)
        self.__export_button.setEnabled(False)

        total_layout.addLayout(top_layout)
        total_layout.addLayout(run_layout)
        total_layout.addWidget(self.__result_list)
        total_layout.addWidget(self.__progress_bar)
        total_layout.addLayout(turtle_layout)
        total_layout.addWidget(self.__export_button)

        self.setLayout(total_layout)
        self.setWindowTitle("Serious Numbers")
        self.setWindowIcon(QtGui.QIcon(SUM_ICON)) 

        self.__count = 0 # counter to display the series index
        self.__last_generated_series = None #last generated series that will be displayed with Turtle Graphics

    def startGenereteSeries(self):
        self.__result_list.clear() # clears the result_list 
        self.__count = 0 # restets the counter
        # get values for the series generator from the series_picker and the spin boxes
        series_name = self.__series_picker.itemText(self.__series_picker.currentIndex())
        recursions = int(self.__recursion_spinner.value())
        offset = int(self.__offset_spinner.value())
        multiply = int(self.__multiply_spinner.value())
        
        # thread that generates the numbers from the sequence 
        self.__get_thread = Generate_Thread(series_name, recursions, offset, multiply)
        self.connect(self.__get_thread, QtCore.SIGNAL("addNumber(int)"), self.addNumber)
        self.connect(self.__get_thread, QtCore.SIGNAL("finished()"), self.stopThread)

        self.__last_generated_series = series_name

        self.__get_thread.start()

        # setting while the series generator thread is running
        self.__progress_bar.setMaximum(recursions)
        self.__progress_bar.setValue(0)
        self.__stop_button.setEnabled(True)
        self.__generate_button.setEnabled(False)
        self.__turtle_runner.setEnabled(False)
        self.__export_button.setEnabled(False)
        self.__stop_button.clicked.connect(self.__get_thread.terminate)

    def addNumber(self, num):
        """
        adds the last number generated in the thread to the result list and updates the progress bar

        :param num: number to add
        :type num: int
        """
        self.__count += 1
        self.__result_list.addItem("{}:{}".format(self.__count, num))
        self.__progress_bar.setValue(self.__progress_bar.value() + 1)

    def displayTurtle(self):
        # gets the list of numbers to display with Turtle Graphics from the result_list
        seq = self.getResults()

        pen_color = self.__color_picker.getPenColor()
        pr = pen_color.toRgb().red()
        pg = pen_color.toRgb().green()
        pb = pen_color.toRgb().blue()

        background_color = self.__color_picker.getBackgroundColor()
        br = background_color.toRgb().red()
        bg = background_color.toRgb().green()
        bb = background_color.toRgb().blue()

        back_hex_color = '#%02x%02x%02x' % (br, bg, bb) # background color from rgb to hex
        pen_hex_color = '#%02x%02x%02x' % (pr, pg, pb)  # pen color from rgb to hex

        # selects the type of series to disply based on the last type of series generated
        if self.__last_generated_series == FIBONACCI_STRING:
            fibonacci.drawFibonacci(seq, pen_hex_color, back_hex_color)
        elif self.__last_generated_series == PADOVAN_STRING:
            padovan.drawPadovan(seq, pen_hex_color, back_hex_color)

    def openColorPicker(self):
        self.__color_picker.open()

    def openFileDialog(self):   
        # opens a QDialogWindow 
        # if a filename is writtten it will generate an output file with the chosen filter(extension)
        filename, filter = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Select output file', dir='.', filter= FILE_FILTERS  )   
        if filename:
            seq = self.getResults()
            """
            takes the fullpatn of the file to generate and the sequence from the result_list 
            generates output based on the chosen extension(txt, json, cvs)
            """
            output.generateOutput(filename,seq)

    def getResults(self):
        """
        returns the series in the result_list

        :rtype: list
        """
        seq = []
        for x in range(self.__result_list.count()):
            split_string = self.__result_list.item(x).text().split(":")
            seq.append(int(split_string[1]))
        return seq           

    def stopThread(self):
        # settings at the end of the thread
        self.__generate_button.setEnabled(True)
        self.__stop_button.setEnabled(False)
        self.__turtle_runner.setEnabled(True)
        self.__progress_bar.setValue(0)
        self.__export_button.setEnabled(True)
        self.__turtle_runner.setEnabled(True)


class Generate_Thread(QtCore.QThread):
    """
    thread where the series numbers are generated one by one 
    the thread is started on pressing the run_button in the main widget
    """

    def __init__(self, series_name, this_recursions, this_offset, this_multiply):
        """
        :param seriesname: type of series to generate (fibonacci or padovan)
        :type series_name: str 

        :type this_recursions, this_offset, this multiply: int
        """
        super(Generate_Thread, self).__init__()

        self.__name = series_name
        self.__recursions = this_recursions
        self.__offset = this_offset
        self.__multiply = this_multiply

    def run(self):
        if self.__name == FIBONACCI_STRING:
            for x in fibonacci.Fib(self.__recursions, self.__offset, self.__multiply): # get numbers one by one with generator
                self.emit(QtCore.SIGNAL('addNumber(int)'), x)
        if self.__name == PADOVAN_STRING:
            for x in padovan.pad(self.__recursions, self.__offset, self.__multiply):   # get numbers one by one with generator  
                self.emit(QtCore.SIGNAL('addNumber(int)'), x)

    def __del__(self):
        self.wait()