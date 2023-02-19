function startVideo(src) {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
            let video = document.getElementById(src);
            if ("srcObject" in video) {
                video.srcObject = stream;
            } else {
                video.src = window.URL.createObjectURL(stream);
            }
            video.onloadedmetadata = function (e) {
                video.play();
            };
            //mirror image
            video.style.webkitTransform = "scaleX(-1)";
            video.style.transform = "scaleX(-1)";
        });
    }
}

let capturingVideo = true;
let frames = 0;

function endFrameCapture() {
    capturingVideo = false;
}

function startFrameCapture(src, dest, dotNetHelper) {
    capturingVideo = true;
    setTimeout(function () { getFrame(src, dest, dotNetHelper); }, 2);
}

async function getFrame(src, dest, dotNetHelper) {
    frames++;
    let video = document.getElementById(src);
    console.log(video);
    let canvas = document.getElementById(dest);
    canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);

    let dataUrl = canvas.toDataURL("image/jpeg");
    document.getElementById("dataSizeLabel").innerHTML = "Frame size: " + dataUrl.length;
    document.getElementById("frameCount").innerHTML = "Frames: " + frames;
    await dotNetHelper.invokeMethodAsync('ProcessImage', dataUrl, dataUrl.length);
    if (capturingVideo) {
        setTimeout(function () { getFrame(src, dest, dotNetHelper); }, 2);
    }
}