function loadAllServersClick() {
  outputDiv = document.querySelector('#start-all-servers-output')
  outputDiv.innerHTML = '<ul></ul>'
  outputList = outputDiv.querySelector('ul')
  loadAllServers((statusMessage) => {
    itemElement = document.createElement("li");
    const { step, details } =statusMessage
    itemElement.innerHTML = `<b>Step ${step}</b> ${details}`
    outputList.appendChild(itemElement)
  })
}

function socketLoaded() {
  document.querySelector('#waiting-to-load-socket-container').style.display = 'none';
  document.querySelector('#main-container').style.display = '';
}

window.addEventListener('load', () => {
  loadAllServersBtn = document.querySelector('#start-all-servers-btn');
  loadAllServersBtn.onclick = loadAllServersClick;
})