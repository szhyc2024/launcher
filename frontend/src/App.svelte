<script lang="ts">
  let username: string = $state("")
  let java_path: string = $state("")
  let minecraft_path: string = $state("")
  let version_path: string = $state("")
  let isolation: boolean = $state(true)
  function launch_game(){
    pywebview.api.launch_game(username, java_path, minecraft_path, version_path, isolation)
  }
  async function select_file(){
    let res: string = await pywebview.api.select_file()
    return res
  }
  async function select_folder(){
    let res: string = await pywebview.api.select_folder()
    return res
  }
</script>

<div id="launch_options">
  <div>
    用户名<input bind:value={username} type="text" placeholder="用户名" />
  </div>
  <div>
    <button onclick={() => select_file().then((value) => java_path=value)}>选择java.exe路径</button>
    {java_path}
  </div>
  <div>
    <button onclick={() => select_folder().then((value) => minecraft_path=value)}>选择minecraft文件夹路径</button>
    {minecraft_path}
  </div>
  <div>
    <button onclick={() => select_folder().then((value) => version_path=value)}>选择版本内路径</button>
    {version_path}
  </div>
  <div>
    是否版本隔离<input bind:checked={isolation} type="checkbox" />
  </div>
  <button onclick={launch_game}>启动</button>
</div>
