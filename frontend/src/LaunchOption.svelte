<script lang="ts">
  interface LauncherConfigs {
    username: string
    java_path: string
    minecraft_path: string
    version_path: string
    isolation: boolean
  }
  let configs: LauncherConfigs = $state({
    username: "",
    java_path: "",
    minecraft_path: "",
    version_path: "",
    isolation: false
  })
  window.addEventListener("beforeunload", async () => {
    await pywebview.api.save_data(configs)
  })
  wait_for_loaded()
  function wait_for_loaded(){
    if(typeof pywebview != 'undefined'){
      init()
    } else {
      setTimeout(wait_for_loaded, 100)
    }
  }
  function init(){
    pywebview.api.load_data().then((value: LauncherConfigs) => configs = value)
  }
  function launch_game(){
    pywebview.api.launch_game(configs.username, configs.java_path, configs.minecraft_path, configs.version_path, configs.isolation)
  }
  function select_file(func: Function){
    return pywebview.api.select_file().then(func)
  }
  function select_folder(func: Function){
    return pywebview.api.select_folder().then(func)
  }
</script>

<div id="launch_options">
  <div>
    用户名<input bind:value={configs.username} type="text" placeholder="用户名" />
  </div>
  <div class="path-group">
    <button onclick={() => select_file((value: string) => configs.java_path=value)}>选择java.exe路径</button>
    <span class="ellipsis" title={configs.java_path}>{configs.java_path}</span>
  </div>
  <div class="path-group">
    <button onclick={() => select_folder((value: string) => configs.minecraft_path=value)}>选择minecraft文件夹路径</button>
    <span class="ellipsis" title={configs.minecraft_path}>{configs.minecraft_path}</span>
  </div>
  <div class="path-group">
    <button onclick={() => select_folder((value: string) => configs.version_path=value)}>选择版本内路径</button>
    <span class="ellipsis" title={configs.version_path}>{configs.version_path}</span>
  </div>
  <div>
    是否版本隔离<input bind:checked={configs.isolation} type="checkbox" />
  </div>
  <button onclick={launch_game}>启动</button>
</div>
