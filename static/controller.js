function onServerStatusReceived(statusMessage) {
  const itemElement = document.createElement("li");
  const { step, details } = statusMessage;
  itemElement.innerHTML = `<b>Step ${step}</b> ${details}`;
  outputList.appendChild(itemElement);

}

async function loadAllServersClick() {
  const outputDiv = window.startAllServersOutput;
  outputDiv.classList.remove('d-none');
  outputDiv.innerHTML = '<ul></ul>';
  outputList = outputDiv.querySelector('ul');
  await loadAllServers(onServerStatusReceived, getDelay())
  setServersLoadedStatus();
}

function setServersLoadedStatus() {
  window.loadAllServersBtn.classList.add('disabled');
  window.stopAllServersBtn.classList.remove('disabled');
}

function setServersTerminatedStatus() {
  window.stopAllServersBtn.classList.add('disabled');
  window.loadAllServersBtn.classList.remove('disabled');
}

function setInitialState(serverStatus) {
  const { jobs_running } = serverStatus;
  if (jobs_running.length > 0) {
    setServersLoadedStatus();
  } else {
    setServersTerminatedStatus();
  }
}

async function stopAllServersClick() {
  await stopAllServers();
  setServersTerminatedStatus();
  const outputDiv = window.startAllServersOutput;
  outputDiv.innerHTML = 'All servers shutdown successfully';
}

function socketLoaded() {
  document.querySelector('#waiting-to-load-socket-container').style.display = 'none';
  document.querySelector('#main-container').style.display = '';
}

function getElementByProcessName(processName) {
  const { serverNames } = window.serverConfig;
  switch(processName) {
    case serverNames.IMAGE_PROCESSING:
      return document.getElementById('image-processing-server-output');
    case serverNames.CAMERA_HEAD:
      return document.getElementById('camera-head-server-output');
    default:
      throw new Error(`Unknown processing name: ${processName}`);
  }
}

function handleServerOutput(data) {
  const { message, server_name } = data;

  const element = getElementByProcessName(server_name);
  const outputHtml = message.replaceAll('\n', '<br />');
  const dateNowString = (new Date()).toISOString();
  element.innerHTML = `<code><div class="row"><div class="col">${dateNowString}</div><div class="col">${outputHtml}</div></div></code>` + element.innerHTML;
}

function loadNewImage(arrayBuffer) {
  const imageElement = document.querySelector('#image-processed');
  // Instead of passing around all the bytes for the iamge, we can just display the image immedaitely, but there are glitches
  // imageElement.src = imageElement.dataset.src + "?" + new Date().getTime();
  imageElement.src = getImageSourceFromArrayBuffer(arrayBuffer);
}

function getDelay() {
  return Number(window.waitBetweenImagesInput.value);
}

window.addEventListener('load', async () => {
  window.loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  window.startAllServersOutput = document.querySelector('#start-all-servers-output');
  window.stopAllServersBtn = document.querySelector('#stop-all-servers-btn');
  window.waitBetweenImagesInput = document.getElementById('wait-time-between-images');

  loadAllServersBtn.onclick = loadAllServersClick;
  window.stopAllServersBtn.onclick = stopAllServersClick;

  window.serverConfig = await readJson('/static/server_config.json');
});