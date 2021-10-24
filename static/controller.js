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
  await loadAllServers(onServerStatusReceived)
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
  switch(processName) {
    case 'image_processing_server':
      return document.getElementById('image-processing-server-output');
    default:
      throw new Error(`Unknown processing name: ${processName}`);
  }
}

function handleServerOutput(processName, outputText) {
  const element = getElementByProcessName(processName);
  const outputHtml = outputText.replaceAll('\n', '<br />');
  const dateNowString = (new Date()).toISOString();
  element.innerHTML = `<code><div class="row"><div class="col">${dateNowString}</div><div class="col">${outputHtml}</div></div></code>` + element.innerHTML;
}

function loadNewImage(arrayBuffer) {
  const imageElement = document.querySelector('#image-processed');
  // Instead of passing around all the bytes for the iamge, we can just display the image immedaitely, but there are glitches
  // imageElement.src = imageElement.dataset.src + "?" + new Date().getTime();
  imageElement.src = getImageSourceFromArrayBuffer(arrayBuffer);
}

window.addEventListener('load', () => {
  window.loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  window.startAllServersOutput = document.querySelector('#start-all-servers-output');
  window.stopAllServersBtn = document.querySelector('#stop-all-servers-btn');

  loadAllServersBtn.onclick = loadAllServersClick;
  window.stopAllServersBtn.onclick = stopAllServersClick;
});