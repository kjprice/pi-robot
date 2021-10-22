function loadAllServersClick() {
  const outputDiv = window.startAllServersOutput;
  outputDiv.classList.remove('d-none');
  outputDiv.innerHTML = '<ul></ul>';
  outputList = outputDiv.querySelector('ul');
  loadAllServers((statusMessage) => {
    const itemElement = document.createElement("li");
    const { step, details } = statusMessage;
    itemElement.innerHTML = `<b>Step ${step}</b> ${details}`;
    outputList.appendChild(itemElement);
  }).then(() => {
    window.loadAllServersBtn.classList.add('disabled');
    window.stopAllServersBtn.classList.remove('disabled');
  });
}

async function stopAllServersClick() {
  await stopAllServers();
  window.stopAllServersBtn.classList.add('disabled');
  window.loadAllServersBtn.classList.remove('disabled');
  const outputDiv = window.startAllServersOutput;
  outputDiv.innerHTML = 'All servers shutdown successfully';
}

function socketLoaded() {
  document.querySelector('#waiting-to-load-socket-container').style.display = 'none';
  document.querySelector('#main-container').style.display = '';
}

window.addEventListener('load', () => {
  window.loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  window.startAllServersOutput = document.querySelector('#start-all-servers-output');
  window.stopAllServersBtn = document.querySelector('#stop-all-servers-btn');

  loadAllServersBtn.onclick = loadAllServersClick;
  window.stopAllServersBtn.onclick = stopAllServersClick;
})