# 🧬 OAK Gesture Plugin for PyMOL

System pozwala na sterowanie molekułami w **PyMOL** przy użyciu gestów dłoni rozpoznawanych przez kamerę **OAK-D**.

---

## 🛠 Co pobrać?

Z repozytorium **pobierasz tylko**:

✅ `gesture_utils.py`  
✅ `oak_plugin.py`  
✅ `requirements.txt`

👉 **Umieść je razem w nowym folderze**, np. `OAK_plugin_pyqt_user/`

---

## 🧪 Utwórz środowisko (env)

Najlepiej otwórz ten folder w **PyCharm** — automatycznie zaproponuje stworzenie środowiska wirtualnego (venv).  
Jeśli nie, możesz to zrobić ręcznie w terminalu:

```bash
python -m venv env
env\Scripts\activate       # Windows
source env/bin/activate      # Linux/Mac
pip install -r requirements.txt
```

> 📌 Upewnij się, że masz zainstalowane:
> `opencv-python`, `pyautogui`, `mediapipe`, `depthai`

---

## ⚠️ Zmień ścieżki w `__init__.py` (ZIP pluginu)

W folderze `OAKGesturePlugin/OAKGesturePlugin/__init__.py` znajdują się trzy ważne ścieżki:

```python
python_path = os.path.abspath("C:/SCIEZKA_DO/env/Scripts/python.exe")
script_path = os.path.abspath("C:/SCIEZKA_DO/oak_plugin.py")
ui_file = os.path.abspath("C:/SCIEZKA_DO/OAKGesturePlugin/demowidget.ui")
```

🔴 **Musisz je zmienić ręcznie na swoje lokalne ścieżki**, ponieważ PyMOL oczekuje tych danych do uruchomienia pluginu.

- `python_path` – do pliku `python.exe` z utworzonego środowiska `env`
- `script_path` – do skryptu `oak_plugin.py`
- `ui_file` – do pliku `demowidget.ui`, który znajduje się wewnątrz folderu ZIP

---

## 🗜 Przygotowanie ZIP dla PyMOL

📦 PyMOL oczekuje pliku `.zip` w strukturze pluginu. W tym celu:

1. Upewnij się, że struktura wygląda tak:

```
OAKGesturePlugin/
└── OAKGesturePlugin/
    ├── __init__.py
    └── demowidget.ui
```

2. Spakuj cały folder `OAKGesturePlugin` (ten zawierający podfolder z tym samym prefiksem) jako:  
   **`OAKGesturePlugin.zip`**

> ⚠️ Nie spakuj tylko plików – spakuj **cały folder `OAKGesturePlugin/`**, aby PyMOL mógł go prawidłowo zainstalować.
    

---

## ✅ Instalacja w PyMOL

1. Uruchom PyMOL  
2. Przejdź do: `Plugin > Plugin Manager > Install`  
3. Wskaż utworzony plik `OAKGesturePlugin.zip`  
4. Kliknij **Install**  
5. Uruchom plugin z: `Plugin > Installed Plugins > OAK Plugin (PyQt)`  
6. Jeśli kamera OAK-D nie jest podłączona, w konsoli pojawi się odpowiedni komunikat – oznacza to, że plugin został uruchomiony poprawnie.Jeśli zamiast tego pojawi się inny błąd, najprawdopodobniej PyMOL nie rozpoznał struktury pluginu  w archiwum .zip. W takim przypadku upewnij się, że plik .zip został spakowany w poprawnej strukturze.

---

## ✋ Gesty – mapa akcji

| Akcja       | Mysza            | Gest dłoni                                              |
|-------------|------------------|----------------------------------------------------------|
| **ROTA**    | Lewy przycisk    | 👌 OK – kciuk + wskazujący, środkowy wyprostowany       |
| **MOVE**    | Środkowy         | ✌️ V – wskazujący + środkowy                            |
| **MOV-Z**   | Prawy            | 🖐 Cztery palce wyprostowane, kciuk schowany            |
| **SLAB UP** | Scroll w górę    | L-gest – wskazujący w górę, kciuk w bok                 |
| **SLAB DOWN**| Scroll w dół    | ✊ Zaciśnięta pięść z kciukiem w bok (180°)             |

---

## ❓ Dlaczego plugin uruchamia zewnętrzny skrypt?

PyMOL – zwłaszcza w wersji instalowanej z Anacondy – **może nie obsługiwać bibliotek takich jak `mediapipe` i `depthai`**.  
Z tego powodu plugin uruchamia zewnętrzny proces Pythona przy użyciu `subprocess`.

---

## 👤 Autor

**eXegiMonumentum**  
Politechnika Rzeszowska (PRz), index 167128  
Projekt: AI + Gesty dłoni + Kamera OAK-D + PyMOL

---
