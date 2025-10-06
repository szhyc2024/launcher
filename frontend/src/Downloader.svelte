<script lang="ts">
  let file_path = $state("")
  let url = $state("")
  let progress = $state(0)
  wait_for_loaded()
  function wait_for_loaded(){
    if(typeof pywebview == "undefined"){
      setTimeout(wait_for_loaded, 100)
    }
  }
  function download_file(url: string, path: string){
    pywebview.api.download_file(url, path)
    setTimeout(progress_callback, 100)
  }
  function progress_callback(){
    pywebview.api.query_progress().then((val) => progress = val)
    if(progress == 100){
      progress = 0
      return
    }
    setTimeout(progress_callback, 100)
  }
  function select_folder(func: Function){
    return pywebview.api.select_folder().then(func)
  }
</script>
<div id="downloader">
  <div class="flex-group">
    <button onclick={() => select_folder((value: string) => file_path=value)}>选择下载位置</button>
    <span class="ellipsis" title={file_path}>{file_path}</span>
  </div>
  <div>
    下载URL<input bind:value={url} type="text" placeholder="URL" />
  </div>
  <progress max="100" value={progress.toString()}></progress>
  <button onclick={() => download_file(url, file_path)} disabled={progress!=100&&progress!=0}>开始下载</button>
</div>