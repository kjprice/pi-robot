function loadAllServersClick() {
  const originalButtonclass = window.loadAllServersBtn.className;
  window.loadAllServersBtn.className='btn btn-warning';
  outputDiv = document.querySelector('#start-all-servers-output');
  outputDiv.innerHTML = '<ul></ul>';
  outputList = outputDiv.querySelector('ul');
  loadAllServers((statusMessage) => {
    const itemElement = document.createElement("li");
    const { step, details } = statusMessage;
    itemElement.innerHTML = `<b>Step ${step}</b> ${details}`;
    outputList.appendChild(itemElement)
  }).then(() => {
    window.loadAllServersBtn.className = originalButtonclass;
  })
}

function socketLoaded() {
  document.querySelector('#waiting-to-load-socket-container').style.display = 'none';
  document.querySelector('#main-container').style.display = '';
}

window.addEventListener('load', () => {
  window.loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  loadAllServersBtn.onclick = loadAllServersClick;
})