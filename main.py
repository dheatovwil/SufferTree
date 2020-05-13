import webbrowser
import gen_json
import threading
import os


def run():
    os.system("python -m http.server")


def simple_start(root):
    gen_json.main(root)
    t = threading.Thread(target=run, daemon=True).start()
    webbrowser.open("localhost:8000/index.html", new=1)
    t.join()
