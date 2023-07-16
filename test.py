import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox
from functionPlotter import MathFunctionApp


@pytest.fixture
def app(qtbot):
    math_app = MathFunctionApp()
    math_app.show()
    qtbot.addWidget(math_app)
    yield math_app
    math_app.close()


def test_negative_numbers_in_max_input(app, qtbot):
    app.function_input.setText("x")
    # Enter a negative number for max_input
    app.max_input.setText("-5")
    app.min_input.setText("0")
    # Click the plot button
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Check if the error dialog is displayed
    error_dialog = app.error_dialog
    assert error_dialog.isVisible()
    assert error_dialog.text() == "'Max of x' should be greater than 'Min of x'."

    # Close the error dialog
    qtbot.mouseClick(error_dialog.button(QMessageBox.Ok), Qt.LeftButton)


def test_invalid_function_input(app, qtbot):
    # Enter an invalid function
    app.function_input.setText("w")

    app.max_input.setText("5")
    app.min_input.setText("0")

    # Click the plot button
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Check if the error dialog is displayed
    error_dialog = app.error_dialog
    assert error_dialog.isVisible()
    assert (
            error_dialog.windowTitle() == "Function Error!"
    )

    # Close the error dialog
    qtbot.mouseClick(error_dialog.button(QMessageBox.Ok), Qt.LeftButton)


if __name__ == "__main__":
    pytest.main(["-v"])
