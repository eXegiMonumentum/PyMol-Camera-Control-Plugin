import os
import subprocess
from pymol.plugins import addmenuitemqt

dialog = None

def __init_plugin__(app=None):
    addmenuitemqt('OAK Plugin (PyQt)', run_plugin_gui)

def run_plugin_gui():
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi
    global dialog

    if dialog is None:
        dialog = QtWidgets.QDialog()
        uifile = os.path.join(os.path.dirname(__file__), 'demowidget.ui')
        form = loadUi(uifile, dialog)

        def run():
            print("▶ Uruchamiam oak_plugin.py przez subprocess!")

            python_path = os.path.abspath(
                "C:/Users/LENOVO/Desktop/Plugin/OakGesturePlugin/OAK_plugin_pyqt/env/Scripts/python.exe"
            )
            script_path = os.path.abspath(
                "C:/Users/LENOVO/Desktop/Plugin/OakGesturePlugin/OAK_plugin_pyqt/oak_plugin.py"
            )

            try:
                subprocess.Popen([python_path, script_path])
                print("🌿 Oak gesture system started.")
            except Exception as e:
                print(f"❌ Failed to start gesture system: {e}")

        form.button_start.clicked.connect(run)

    dialog.show()
