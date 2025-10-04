import webview
import mmcll
import subprocess
index_path = "./frontend/dist/index.html"

class Api:
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


webview.create_window("启动器", height=400, width=800, url=index_path, js_api=Api())
webview.start(debug=True)