from src import App
import webview
import os
import sys

if getattr(sys, "frozen", False):
    WORKING_DIR = os.path.dirname(sys.executable)
    print("WORKING_DIR: ", WORKING_DIR)
else:
    WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
    print("WORKING_DIR: ", WORKING_DIR)

app = App(WORKING_DIR)

if __name__ == "__main__":
    try:
        webview.create_window("E-Rapor SMK Perwira", app, maximized=True)
        webview.start(gui="edgechromium")
    except webview.errors.WebViewException as e:
        print("Error: ", e)
    # app.run() # TODO delete for production
