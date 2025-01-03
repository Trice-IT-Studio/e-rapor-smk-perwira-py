from src import App
import webview
import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
app = App(WORKING_DIR)

if __name__ == "__main__":
    try:
        webview.create_window("E-Rapor SMK Perwira", app, maximized=True)
        webview.start(gui="qt")
    except webview.errors.WebViewException as e:
        print("Error: ", e)
    # app.run() # TODO delete for production
