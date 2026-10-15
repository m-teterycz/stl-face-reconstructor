import sys
import ctypes
from pathlib import Path

from PySide6 import QtWidgets, QtGui, QtCore
from gui import worker

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "stl_face_reconstructor.app"
    )

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("STL to STEP Converter")
        self.resize(450, 280)

        self.selected_file = ""

        main_layout = QtWidgets.QVBoxLayout(self)

        self.title = QtWidgets.QLabel("STL to STEP Converter")
        self.file_label = QtWidgets.QLabel("No file selected")

        self.browse_button = QtWidgets.QPushButton("Browse")
        self.convert_button = QtWidgets.QPushButton("Convert")

        main_layout.addWidget(self.title)
        main_layout.addWidget(self.file_label)
        main_layout.addWidget(self.browse_button)

        self.tabs = QtWidgets.QTabWidget()

        measurement_tab = QtWidgets.QWidget()
        measurement_layout = QtWidgets.QFormLayout(measurement_tab)

        self.measurement_definition = QtWidgets.QComboBox()
        self.measurement_definition.addItems([
            "Millimeters",
            "Meters"
        ])

        measurement_layout.addRow(
            "Measurement Definition:",
            self.measurement_definition
        )

        self.tabs.addTab(measurement_tab, "Measurement Definition")
        main_layout.addWidget(self.tabs)

        main_layout.addWidget(self.convert_button)

        self.browse_button.clicked.connect(self.select_file)
        self.convert_button.clicked.connect(self.convert)

    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select STL File",
            "",
            "STL Files (*.stl);;All Files (*)"
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.setText(Path(file_path).name)

    def convert(self):
        if not self.selected_file:
            QtWidgets.QMessageBox.warning(
                self, "No File Selected",
                "Please select an STL file first."
            )
            return

        path = Path(self.selected_file)

        if path.suffix.lower() != ".stl":
            QtWidgets.QMessageBox.warning(
                self, "Invalid File",
                "Please select an STL file (.stl)."
            )
            return

        file_dir = str(path.parent)
        file_name = path.stem

        measurement = self.measurement_definition.currentText()

        if measurement == "Millimeters":
            prefix = "MILLI"
            unit = "METRE"
        else:
            prefix = "$"
            unit = "METRE"

        
        self.convert_button.setEnabled(False)
        self.file_label.setText("Converting...")

        try:
            worker.stl_to_step(
                file_dir,
                file_name,
                prefix,
                unit
            )

            self.file_label.setText("Conversion successful!")
        
        except Exception as error:
            self.file_label.setText("Conversion failed!")
            QtWidgets.QMessageBox.critical(
                self, "Conversion Error",
                f"Could not convert the STL file:\n\n{error}"
            )

        finally:
            self.convert_button.setEnabled(True)

def display():
    app = QtWidgets.QApplication.instance()

    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    icon_path = Path(__file__).resolve().parent / "app.ico"
    icon = QtGui.QIcon(str(icon_path))

    if icon.isNull():
        print(f"Could not load icon: {icon_path}")

    app.setWindowIcon(icon)

    window = MyWidget()
    window.setWindowIcon(icon)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(display())