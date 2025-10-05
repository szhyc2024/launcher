import webview
import mmcll
import subprocess
import json
import os
import DownloadKit
import time
import math

index_path = "./frontend/dist/index.html"
download_kit = DownloadKit.DownloadKit()

class Api:
    def __init__(self):
        self.download_progress = 0

    def launch_game(self, username, java_path, minecraft_path, version_path, isolation):
        game_path = version_path if isolation else minecraft_path
        uuid = mmcll.MainClass.generate_bukkit_uuid(username)
        account = mmcll.LaunchAccount.new_offline(username, uuid)
        option = mmcll.LaunchOption(account, java_path, minecraft_path, version_path, game_path)
        launch = mmcll.launch_game(option, subprocess.run)
        print(java_path, minecraft_path, version_path)
        return launch
    
    def select_file(self):
        try:
            res = webview.windows[0].create_file_dialog(
                dialog_type=webview.FileDialog.OPEN
            )
            return res[0] if res else ""
        except Exception as e:
            print("错误", e)
            return ""
    
    def select_folder(self):
        try:
            res = webview.windows[0].create_file_dialog(
                dialog_type=webview.FileDialog.FOLDER
            )
            return res[0] if res else ""
        except Exception as e:
            print("错误", e)
            return ""
    
    def save_data(self, data):
        with open('launcher_config.json', 'w') as file:
            json.dump(data, file)
    
    def load_data(self):
        if not os.path.isfile('launcher_config.json'):
            return {
                "username": "",
                "java_path": "",
                "minecraft_path": "",
                "version_path": "",
                "isolation": False,
            }
        with open('launcher_config.json', 'r') as file:
            data = json.load(file)
        return data
    
    def download_file(self, url, path):
        misson = download_kit.add(file_url=url, save_path=path)
        self.download_progress = 0
        while self.download_progress != 100:
            if misson.rate is None:
                self.download_progress = 0
            else:
                self.download_progress = math.floor(misson.rate)
            time.sleep(0.1)
    
    def query_progress(self):
        return self.download_progress

win = webview.create_window("启动器", height=300, width=800, url=index_path, js_api=Api())
webview.start(debug=True)