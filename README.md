
# OakGesturePlugin for PyMOL

Plugin do PyMOLa umożliwiający sterowanie molekułami za pomocą gestów dłoni z użyciem kamery OAK-D i technologii MediaPipe.  

---

## 📁 Struktura repozytorium

```
pymol-gesture-plugin/
└── Plugin/
    ├── OakGesturePlugin.zip            ← ZIP pluginu do załadowania w PyMOL
    ├── OakGesturePlugin/              ← Rozpakowana zawartość ZIP-a (GUI pluginu)
    │   ├── __init__.py                ← Kluczowy plik: zmieniasz tu ścieżki!
    │   └── demowidget.ui              ← Interfejs graficzny (PyQt)
    │
    └── OAK_plugin_pyqt/               ← Silnik rozpoznawania gestów
        ├── gesture_utils.py           ← Funkcje rozpoznające gesty
        ├── oak_plugin.py              ← Główny skrypt rozpoznający gesty
        ├── requirements.txt           ← Lista paczek   
   
```

---

## 🛠 Co pobrać?

Z repozytorium **pobierasz tylko**:

✅ `gesture_utils.py`  
✅ `oak_plugin.py`

👉 **Umieść je razem w nowym folderze**, np. `OAK_plugin_pyqt_user/`

---

## 🧪 Utwórz środowisko (env)

Najlepiej otwórz ten folder w **PyCharm** — automatycznie zaproponuje stworzenie środowiska wirtualnego (venv).  
Jeśli nie, możesz to zrobić ręcznie w terminalu:

```bash
python -m venv env
env\Scripts\activate     # Windows
source env/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

> 📌 Upewnij się, że masz zainstalowane:
> `opencv-python`, `pyautogui`, `mediapipe`, `depthai`

---

## ⚠️ Zmień ścieżki w `__init__.py` (ZIP pluginu)

W środku `OakGesturePlugin/__init__.py` znajdują się dwie ścieżki:

```python
python_path = os.path.abspath("C:/SCIEZKA_DO/env/Scripts/python.exe")
script_path = os.path.abspath("C:/SCIEZKA_DO/oak_plugin.py")
```

🔁 Zamień je na **lokalne ścieżki** do:

- Twojego `env`
- Twojego `oak_plugin.py`

---

## ✅ Instalacja w PyMOL

1. Pobierz ZIP -- > To w nimy zmienić ścieżki w __init__:  
   [OakGesturePlugin.zip](https://github.com/eXegiMonumentum/pymol-gesture-plugin/raw/main/Plugin/OakGesturePlugin.zip)

2. W PyMOLu:
   - `Plugin > Plugin Manager > Install`
   - Wybierz ZIP, w którym zmieniłeś ścieżki na poprawne (ścieżki do swojego venv gdzie ma odpalić się skrypt oraz ścieżka do skryptu oak_plugin.py) 
   - Kliknij **Install**

3. Uruchom:
   - `Plugin > Installed Plugins > OAK Plugin (PyQt)`
   - Kliknij **Start**

---

## ✋ Gesty

| Akcja       | Mysza        | Gest                                                     |
|-------------|--------------|-----------------------------------------------------------|
| ROTA        | Lewy przycisk| 👌 OK – kciuk + wskazujący                               |
| MOVE        | Środkowy     | ✌️ V – wskazujący + środkowy                            |
| MOV-Z       | Prawy        | 🖐 4 palce wyprostowane, kciuk schowany                 |
| SLAB UP     | Scroll ↑     |  L-kształtny (wskazujący w górę, kciuk w bok)         |
| SLAB DOWN   | Scroll ↓     | ✊ Pięść z kciukiem poziomo (180°)                      |

---

## 👨‍💻 Autor: eXegiMonumentum
    PRz.index 167128

Eksperymentalne sterowanie molekułami w PyMOLu przy pomocy AI i gestów dłoni ✨
