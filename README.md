
# OakGesturePlugin for PyMOL## 📦 Szybka instalacja

[Kliknij tutaj, aby pobrać plugin ZIP do PyMOL](https://github.com/eXegiMonumentum/pymol-gesture-plugin/Plugin/OakGesturePlugin.zip)

A PyMOL plugin that enables 3D molecular interaction using hand gestures captured by an OAK-D camera. This plugin provides a GUI interface and communicates with an external gesture recognition system based on Python, MediaPipe, and DepthAI.

## 🔧 Features

- Control PyMOL with gestures:
  - 🖱 Rotate (left click)
  - 🎯 Move (middle click)
  - 🔍 Zoom (right click)
  - 🔃 Scroll (clipping/slabbing)
- Real-time hand tracking via OAK-D camera
- Toggleable gesture tracking and camera preview
- Simple GUI launcher within PyMOL

## 🖐️ Gesture Mapping (for 3-Button Viewing Mode in PyMOL)

| Action       | Mouse Button | Gesture Description                                                  | Effect                              |
|--------------|--------------|-----------------------------------------------------------------------|-------------------------------------|
| **ROTA**     | Left Click   | 👌 “OK” gesture (thumb + index finger touching)                      | Rotate 3D model                     |
| **MOVE**     | Middle Click | ✌️ “V” gesture (index + middle finger extended)                     | Pan the model                      |
| **MOV-Z**    | Right Click  | 🖐 4 fingers extended, thumb folded                                  | Zoom in/out (move along Z axis)    |
| **SLAB UP**  | Scroll Up    |  Index finger up, thumb 90° to the side, others folded (L-shape) | Raise clipping front plane         |
| **SLAB DOWN**| Scroll Down  | ✊ Fist with thumb extended horizontally (180° from palm)            | Lower clipping back plane          |

## 🧰 Requirements

- PyMOL (with plugin support)
- Python 3.9+
- Anaconda or virtual environment
- [MediaPipe](https://google.github.io/mediapipe/)
- [depthai](https://docs.luxonis.com/)

## 🚀 Usage

1. Clone or download this repository.
2. Set up the Python environment in `OAK_plugin_pyqt/env/` with required packages.
3. Open PyMOL and install the plugin ZIP via:
   ```
   Plugin > Plugin Manager > Install > From File...
   ```
4. Click on the plugin in the PyMOL menu.
5. Press **Start** to launch gesture control.

## 📁 Repository Structure

```
OakGesturePlugin/         <- PyMOL plugin with GUI
  ├── __init__.py
  └── demowidget.ui

OAK_plugin_pyqt/          <- Gesture recognition system
  ├── oak_plugin.py
  ├── gesture_utils.py
  └── env/                <- Virtual environment (optional, not included)
```

## 📦 Dependencies (install in virtual env)

```
pip install opencv-python mediapipe depthai pyautogui
```
