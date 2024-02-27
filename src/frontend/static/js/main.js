$(document).ready(function() {
    const video = document.getElementById('video');
    const countdown = document.getElementById('countdown');
    const capturedImage = document.getElementById('capturedImage');
    let counter;
    function startCountdown() {
        if (counter > 0) {
            countdown.innerText = counter;
            counter--;

            setTimeout(startCountdown, 1000);
        } else {
            captureImage();
        }
    }
    function captureImage() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/png');
        $.ajax({
            url: '/save_images',
            type: 'POST',
            data: { image: imageData, numInJavaScript: numInJavaScript },
            success: function(response) {
            },
            error: function(error) {
                console.error('Error sending images to server:', error);
            }
        });
        setTimeout(startNextIteration, 2000);
    }

    function startNextIteration() {
        if (numInJavaScript > 0) {
            console.log(numInJavaScript)
            if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
            console.log("Let's get this party started")
            }
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    video.srcObject = stream;
                    counter = 5;
                    startCountdown();
                })
                .catch((error) => {
                    console.error('Error accessing webcam:', error);
                });

            numInJavaScript--;
        } else {
            window.location.href = '/result/' + originNum;
        }
    }
    startNextIteration();
});
