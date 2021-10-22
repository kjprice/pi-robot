function loadAllServersClick() {
  const outputDiv = window.startAllServersOutput;
  outputDiv.classList.remove('d-none');
  window.loadAllServersBtn.className='btn btn-warning';
  outputDiv.innerHTML = '<ul></ul>';
  outputList = outputDiv.querySelector('ul');
  loadAllServers((statusMessage) => {
    const itemElement = document.createElement("li");
    const { step, details } = statusMessage;
    itemElement.innerHTML = `<b>Step ${step}</b> ${details}`;
    outputList.appendChild(itemElement)
  }).then(() => {
    window.loadAllServersBtn.className = 'btn btn-outline-success disabled';
    window.stopAllServersBtn.classList.remove('disabled');
  })
}

function socketLoaded() {
  document.querySelector('#waiting-to-load-socket-container').style.display = 'none';
  document.querySelector('#main-container').style.display = '';
}

window.addEventListener('load', () => {
  window.loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  loadAllServersBtn.onclick = loadAllServersClick;
  window.startAllServersOutput = document.querySelector('#start-all-servers-output');

  window.stopAllServersBtn = document.querySelector('#stop-all-servers-btn');
})