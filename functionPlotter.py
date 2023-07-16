# GUI imports

from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QMainWindow,

)
# Plotting imports
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Utilities imports
import numpy as np
import sys
import re

allow_list = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    '/',
    '+',
    '*',
    '^',
    '-'
]

replacements = {
    "sin": "np.sin",
    "cos": "np.cos",
    "exp": "np.exp",
    "sqrt": "np.sqrt",
    "^": "**"
}


class MathFunctionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 600, 400)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.function_label = QLabel("Math Function: ", self)
        self.function_label.setGeometry(20, 20, 100, 20)

        self.function_input = QLineEdit(self)
        self.function_input.setGeometry(130, 20, 200, 20)

        self.max_label = QLabel("Enter Max of X : ", self)
        self.max_label.setGeometry(20, 50, 100, 20)

        self.max_input = QLineEdit(self)
        self.max_input.setGeometry(130, 50, 100, 20)

        self.min_label = QLabel("Enter Min of X : ", self)
        self.min_label.setGeometry(20, 80, 100, 20)

        self.min_input = QLineEdit(self)
        self.min_input.setGeometry(130, 80, 100, 20)

        self.plot_button = QPushButton("Plot", self)
        self.plot_button.setGeometry(20, 120, 80, 25)
        self.plot_button.clicked.connect(self.plot_function)

        self.error_dialog = QMessageBox()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_input)
        self.layout.addWidget(self.max_label)
        self.layout.addWidget(self.max_input)
        self.layout.addWidget(self.min_label)
        self.layout.addWidget(self.min_input)
        self.layout.addWidget(self.plot_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def plot_function(self):

        function = self.function_input.text()
        for word in re.findall("[a-zA-Z_]+", function):
            if word not in allow_list:
                self.error_dialog.setWindowTitle("Function Error!")
                self.error_dialog.setText(
                    f"'{word}' is forbidden to use in math expression.\nOnly functions of 'x' are allowed.\ne.g., "
                    f"5*x^3 + 2/x - 1\nList of allowed words: {', '.join(allow_list)}")
                self.error_dialog.show()
                return

        for old, new in replacements.items():
            function = function.replace(old, new)

        if "x" not in function:
            function = f"{function}+0*x"

        x_max = float(self.max_input.text())
        x_min = float(self.min_input.text())

        if x_max <= x_min:
            self.error_dialog.setWindowTitle("Max of x Error")
            self.error_dialog.setText("'Max of x' should be greater than 'Min of x'.")
            self.error_dialog.show()
            return

        x = np.linspace(x_min, x_max, 100)

        y = eval(function)
        self.figure.clear()
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        self.canvas.draw()


app = QApplication(sys.argv)
window = MathFunctionApp()
window.show()
app.exec_()
