import webbrowser
from threading import Thread

from .backend import PORT, run_server

# 在背景執行伺服器
Thread(target=run_server).start()
# 開啟瀏覽器
webbrowser.open(f'http://localhost:{PORT}')
