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
  let is_launching = $state(false)
  let launching_hint = $state("开始你的第一次启动吧！")
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
    is_launching = true
    pywebview.api.launch_game(configs.username,
    configs.java_path,
    configs.minecraft_path,
    configs.version_path,
    configs.isolation).then((result: [boolean, number]) => {
      is_launching = false
      if(!result[0]){
        launching_hint = "已有游戏正在启动中，请稍后再试。"
        is_launching = true
        return
      }
      if(result[1] != 0){
        launching_hint = "游戏启动失败，错误码："+result[1]
      } else {
        launching_hint = "启动成功！"
      }
    })
  }
  function select_file(func: Function){
    return pywebview.api.select_file().then(func)
  }
  function select_folder(func: Function){
    return pywebview.api.select_folder().then(func)
  }
</script>

<div id="launch_options" class="card py-3" style="width: fit-content;">
  <div class="mx-auto px-3 my-2 input-group">
    <span class="input-group-text">用户名</span>
    <input bind:value={configs.username} type="text" placeholder="用户名" class="form-control"/>
  </div>
  <div class="row mx-auto my-2">
    <button class="btn btn-primary col-12" onclick={() => select_file((value: string) => configs.java_path=value)}>选择java.exe路径</button>
    <span class="ellipsis col" title={configs.java_path}>{configs.java_path}</span>
  </div>
  <div class="row mx-auto my-2">
    <button class="btn btn-primary col-12" onclick={() => select_folder((value: string) => configs.minecraft_path=value)}>选择minecraft文件夹路径</button>
    <span class="ellipsis col" title={configs.minecraft_path}>{configs.minecraft_path}</span>
  </div>
  <div class="row mx-auto my-2">
    <button class="btn btn-primary col-12" onclick={() => select_folder((value: string) => configs.version_path=value)}>选择版本内路径</button>
    <span class="ellipsis col" title={configs.version_path}>{configs.version_path}</span>
  </div>
  <div class="mx-auto my-2 form-check">
    <input bind:checked={configs.isolation} type="checkbox" class="form-check-input" />
    <span class="form-check-label">是否版本隔离</span>
  </div>
  <div class="row mx-auto my-2">
    <button class="btn btn-primary col-12" onclick={launch_game}>启动</button>
  </div>
  <div class="row">
    <div class="col text-center">
      <span class="text-info">{launching_hint}</span>
    </div>
  </div>
</div>
