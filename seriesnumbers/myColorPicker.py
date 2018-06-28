
from PySide import QtGui
from PySide import QtCore
import sys

class MyColorPickerDialog(QtGui.QDialog):

    def __init__(self):

        super(MyColorPickerDialog, self).__init__()

        self.__background_color = QtGui.QColor(0,0,0)
        self.__pen_color = QtGui.QColor(255,255,255)

        general_layout = QtGui.QVBoxLayout()

        self.__rainbow_gradient = ColorPicker()
        self.__rainbow_gradient_widget = self.wrapWidget(self.__rainbow_gradient, 10, 15)
        self.__color_gradient = ColorGradient(self.__rainbow_gradient)
        self.__color_gradient_widget = self.wrapWidget(self.__color_gradient, 5, 15)
        colors_layout = QtGui.QHBoxLayout()

        colors_layout.addWidget(self.__rainbow_gradient_widget, stretch = 1)
        colors_layout.addWidget(self.__color_gradient_widget, stretch = 4)

        options_layout = QtGui.QFormLayout()
        options_layout.setSpacing(0)
        self.__background_button = QtGui.QPushButton()
        self.__background_button.clicked.connect(self.updateBackground)
        self.__pen_button = QtGui.QPushButton()
        self.__pen_button.clicked.connect(self.UpdatePen)
        options_layout.addRow("Background", self.__background_button)
        options_layout.addRow("Line", self.__pen_button)
         
        apply_layout = QtGui.QHBoxLayout()
        apply_layout.addSpacing(150)
        self.apply_button = QtGui.QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.close)
        apply_layout.addWidget(self.apply_button)
        apply_layout.addSpacing(150)

        general_layout.addLayout(colors_layout, stretch = 5)
        general_layout.addLayout(options_layout, stretch = 1)
        general_layout.addLayout(apply_layout, stretch = 1)

        self.setButtonColor(self.__background_button, self.__background_color, 0, 0, 0)
        self.setButtonColor(self.__pen_button, self.__pen_color, 255, 255, 255)

        self.setLayout(general_layout)
        self.setGeometry(60,70,300,350)
        self.setWindowTitle("My Sad Color Picker")

    def setButtonColor(self, button, color, r, g, b):
        """
        :param button: background or line button
        :type button: QPushButton

        :param color: background or line color
        :type color: QColor

        :param r, g, b: new color Rgb coordinates
        :type r, g, b: int
        """
        new_style = "background-color:rgb({}, {}, {})".format(r,g,b)
        button.setStyleSheet(new_style)
        color = QtGui.QColor(r, g, b)

    def updateBackground(self):
        # updates the color selected for the background and calls for change of the color of the Background button
        new_color = self.__color_gradient.selected_color
        r = new_color.toRgb().red()
        g = new_color.toRgb().green()
        b = new_color.toRgb().blue()
        self.__background_color = new_color
        self.setButtonColor(self.__background_button, self.__background_color, r, g, b)

    def UpdatePen(self):
        # updates the color selected for the pen and calls for change of the color of the Line button
        new_color = self.__color_gradient.selected_color
        r = new_color.toRgb().red()
        g = new_color.toRgb().green()
        b = new_color.toRgb().blue()
        self.__pen_color = new_color
        self.setButtonColor(self.__pen_button, self.__pen_color, r, g, b )

    def getPenColor(self):
        color = self.__pen_color
        return color

    def getBackgroundColor(self):
        color = self.__background_color
        return color

 

    def wrapWidget(self, widget, v_space, h_space):
        """
        Adds border to the color gradient widget

        :param widget: the widget to wrap
        :type widget: QWidget

        :rtype: QWIdget
        """
        wrapped_widget = QtGui.QWidget()
        h_layout = QtGui.QHBoxLayout()
        v_layout = QtGui.QVBoxLayout()
        v_layout.addSpacing(v_space)
        v_layout.addWidget(widget)
        v_layout.addSpacing(v_space)
        h_layout.addSpacing(h_space)
        h_layout.addLayout(v_layout)
        h_layout.addSpacing(h_space)
        wrapped_widget.setLayout(h_layout)
        return wrapped_widget

class ColorGradient(QtGui.QWidget): 
    """
    four corner color gredient widget from wich you can select the color to apply
    to the line or the background of the Turtle Graphics
    """
    def __init__(self, color_picker):
        """
        :param color_picker: "ranibow gradient" that signals the main color change
        :type color_picker: QWidget
        """
        super(ColorGradient,self).__init__()

        self.__color_picker = color_picker
        self.__color_picker.color_changed.connect(self.updateColor)
        self.__gradient_image = None
        self.__main_color = QtGui.QColor(255, 255, 255)
        self.__selector_y = 0.5
        self.__selector_x = 0.5
        self.selected_color = QtGui.QColor(0, 0, 0)
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.getNewImage)

    def showEvent(self, event):
        self.updateColor(self.__color_picker.getColorSelected())

    def resizeEvent(self, event):
        self.__timer.start(500)

    def getNewImage(self):
        self.__gradient_image = QtGui.QPixmap().grabWidget(self).toImage()

    def updateColor(self, color):
        self.__main_color = color
        self.getNewImage()
        self.updatePixelColor()
        self.repaint()

    def paintEvent(self, event):
        # Override paint event to draw the gradient inside the Widget
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGradient(event,qp)
        qp.end()

    def drawGradient(self,event,qp):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        
        # get Rgb values for the color selected in the "rainbow-gradient"
        r = self.__main_color.toRgb().red()
        g = self.__main_color.toRgb().green()
        b = self.__main_color.toRgb().blue()
        
        # list of colours of the first row of pixels
        top_gradient = self.linearGradient([r, g, b], [255, 255, 255], width/2) 
        # 2-dimensionla list of all the colors in the widget
        color_array = [(self.linearGradient(top_gradient[x], [0, 0, 0], height/2)) for x in range(len(top_gradient))] 
          
        # draw the widget pixel by pixel
        for x in range(width/2):
            for y in range(height/2):
                qp.setPen(QtGui.QColor(color_array[x][y][0], color_array[x][y][1], color_array[x][y][2]))
                # draw four pixel for each color in the color_array
                qp.drawPoint(2*x,     2*y    )
                qp.drawPoint(2*x + 1, 2*y    )
                qp.drawPoint(2*x,     2*y + 1)
                qp.drawPoint(2*x + 1, 2*y + 1)
        
        # draw color selector
        qp.drawEllipse(self.__selector_x*width - 10, self.__selector_y*height - 10 , 20, 20)

    def linearGradient(self,start_rgb, finish_rgb, n):
        """
        takes a start and finish color and returns a list of the interpolation between the two with resolution n

        :type start_rgb, finish_rgb: list[int, int, int]
        :type n: int

        :rtype: list[n*[int, int, int]]
        """
        rgb_list = [start_rgb]

        for t in range(1, n):
            current_color = [int((start_rgb[j]) + (float(t)/(n-1))*(finish_rgb[j] - start_rgb[j])) for j in range(3)]
            rgb_list.append(current_color)

        return rgb_list
    
    def mouseReleaseEvent(self, event):
        """
        recalculates the position of the cursor and the pixel 
        at the end repaints the widget
        """
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        cursor = QtGui.QCursor()
        new_pos = self.mapFromGlobal(cursor.pos())
        x = new_pos.x()
        y = new_pos.y()
        self.__selector_y = y/float(height) # normalized value of the y position
    	self.__selector_x = x/float(width)  #normalised value of the x position
        self.updatePixelColor()
        self.repaint()

    def updatePixelColor(self):
        # changes the currently selected color to the the new one picked 
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        pixel_pos = QtCore.QPoint(self.__selector_x*width, self.__selector_y*height)
        self.selected_color = QtGui.QColor(self.__gradient_image.pixel(pixel_pos))



class ColorPicker(QtGui.QWidget):

    color_changed = QtCore.Signal(QtGui.QColor) # signal that changes the main color of the four points color picker

    def __init__(self):
        super(ColorPicker,self).__init__()

        self.__selector_y = 0.1
        self.__picker_image = None
        self.__color_selected = QtGui.QColor(255,0,0)

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.getNewImage)

    def paintEvent(self,event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawColorPicker(event,qp)
        qp.end()

    def drawColorPicker(self,event,qp):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        gradient = QtGui.QLinearGradient(QtCore.QPointF(width/2, 0), QtCore.QPointF(width/2, height))
        gradient.InterpolationMode(QtGui.QGradient.ComponentInterpolation)
        gradient.setColorAt(0,    QtGui.QColor(255, 0,   0))   #           
        gradient.setColorAt(0.16, QtGui.QColor(255, 255, 0))   #          *RAINBOW*
        gradient.setColorAt(0.32, QtGui.QColor(0,   255, 0))   #           * * * *
        gradient.setColorAt(0.48, QtGui.QColor(0,   255, 255)) #           \(^.^)/
        gradient.setColorAt(0.64, QtGui.QColor(0,   0,   255)) #             [0]
        gradient.setColorAt(0.80, QtGui.QColor(255, 0,   255)) #             / \
        gradient.setColorAt(1,    QtGui.QColor(255, 0,   0))   #          
     
        qp.setBrush(gradient)
        qp.drawRect(0, 0, width, height)
        qp.drawEllipse(0, (self.__selector_y*height - width/6), width, width)

    def mouseReleaseEvent(self, event):
        # updates the poition of the color selector
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        cursor = QtGui.QCursor()
        new_pos = self.mapFromGlobal(cursor.pos()) #position relative to the widget
        x = new_pos.x()
        y = new_pos.y()
        self.__selector_y = y/float(height) # normalized value of the new selector y-pos
        self.updatePixelColor()
        self.repaint() 

    def resizeEvent(self,event):
        self.__timer.start(500) # starts the timer at the end of wich a new color picker image is created
    
    def updatePixelColor(self):
        """
        updates the color and the selector position picked in the "rainbow-gradient"
        emits a signal to the four corner gradient widget to update his main color
        """
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        pixel_pos = QtCore.QPoint(width/2, self.__selector_y*height)
        self.__color_selected = QtGui.QColor(self.__picker_image.pixel(pixel_pos))
        self.color_changed.emit(self.__color_selected)

    def getColorSelected(self):
        """
        :rtype: QColor
        """
        color = self.__color_selected
        return color

    def getNewImage(self):
        # generates new image to pick colors from after Resize if resizeEvevnt hasn't been called in 500ms 
        self.__picker_image = QtGui.QPixmap().grabWidget(self).toImage()

    def RegisterSignal(self,obj):
        self.color_changed.connect(obj)


def main():
    app = QtGui.QApplication(sys.argv)
    dialog = MyColorPickerDialog()
    dialog.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()