
// public method for encoding an Uint8Array to base64
// https://stackoverflow.com/questions/11089732/display-image-from-blob-using-javascript-and-websockets
function encodeImage(input) {
  var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  var output = "";
  var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
  var i = 0;

  while (i < input.length) {
      chr1 = input[i++];
      chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index 
      chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

      enc1 = chr1 >> 2;
      enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
      enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
      enc4 = chr3 & 63;

      if (isNaN(chr2)) {
          enc3 = enc4 = 64;
      } else if (isNaN(chr3)) {
          enc4 = 64;
      }
      output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                keyStr.charAt(enc3) + keyStr.charAt(enc4);
  }
  return output;
}

function getImageSourceFromArrayBuffer(arrayBuffer) {
    const bytes = new Uint8Array(arrayBuffer);

    return 'data:image/jpg;base64,' + encodeImage(bytes);
}

// https://stackoverflow.com/questions/19706046/how-to-read-an-external-local-json-file-in-javascript
function readTextFile(file) {
    return new Promise((res, rej) => {
        let fileAlreadyFound = false;
        const rawFile = new XMLHttpRequest();
        rawFile.overrideMimeType("application/json");
        rawFile.open("GET", file, true);
        rawFile.onreadystatechange = () => {
            window.rawFile = rawFile;
            if (rawFile.readyState === 4 && rawFile.status == "200") {
                res(rawFile.responseText);
                fileAlreadyFound = true;
            }
        }
        setTimeout(() => {
            if (!fileAlreadyFound) {
                rej('Timeout');
            }
        }, 2000);
        rawFile.send(null);
    });
}

async function readJson(filepath) {
    const rawFileText = await readTextFile(filepath);
    return JSON.parse(rawFileText);
}