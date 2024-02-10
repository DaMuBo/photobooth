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

        capturedImage.src = canvas.toDataURL('image/png');
        capturedImage.style.display = 'block';

        const imageData = capturedImage.src;
        // Hier können Sie die Bilder weiterverarbeiten, z.B. auf dem Server speichern
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
        // Nächster Durchlauf nach einer Pause von z.B. 2 Sekunden
        setTimeout(startNextIteration, 2000);
    }

    function startNextIteration() {
        if (numInJavaScript > 0) {
            console.log(numInJavaScript)
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    video.srcObject = stream;
                    // Initialen Counter-Wert setzen (z.B., 5 Sekunden)
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
