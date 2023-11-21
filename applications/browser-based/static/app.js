document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('outputCanvas');
    const ctx = canvas.getContext('2d');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            video.play();
        })
        .catch((error) => {
            console.error('Error accessing webcam:', error);
        });

    video.addEventListener('loadeddata', () => {
        setInterval(() => {
            captureAndSendFrame();
        }, 1000); // Adjust the interval as needed
    });

    function captureAndSendFrame() {
       
        const imageData = canvas.toDataURL('image/jpeg', 1); // Convert canvas to base64 data

        // Send imageData to the Python server
        sendDataToServer(imageData);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    }

    function sendDataToServer(imageData) {
        fetch('/predictions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_base64: imageData }),
        })
        .then(response => response.json())
        .then((data) => {
            // Process the results and draw bounding boxes on the canvas
            console.log(data.detections)
            drawBoundingBoxes(data.detections);
        })
        .catch((error) => {
            console.error('Error sending data to server:', error);
        });
    }

    // function drawBoundingBoxes(results) {
    //     // Clear previous bounding boxes
    //     ctx.clearRect(0, 0, canvas.width, canvas.height);

    //     // Draw bounding boxes based on the results received from the server
    //     results.forEach(result => {
    //         ctx.beginPath();
    //         const width = Math.floor((result.box.xMax - result.box.xMin) * canvas.width);
    //         const height = Math.floor((result.box.yMax - result.box.yMin) * canvas.height);
    //         const x = Math.floor(result.box.xMin * canvas.width);
    //         const y = Math.floor(result.box.yMin * canvas.height);
    //         ctx.rect(x, y, width, height);
    //         ctx.lineWidth = 2;
    //         ctx.strokeStyle = 'red';
    //         ctx.fillStyle = 'red';
    //         ctx.stroke();
    //         ctx.fillText(result.label, result.x, result.y - 5);
    //     });
    // }
    // function drawBoundingBoxes(results) {
    //     const video = document.getElementById('webcam');
    //     const canvas = document.getElementById('outputCanvas');
    //     const ctx = canvas.getContext('2d');
    
    //     // Clear previous bounding boxes
    //     // ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    //     // Draw bounding boxes based on the results received from the server
    //     results.forEach(result => {
    //         const scaleX = video.width / canvas.width;
    //         const scaleY = video.height / canvas.height;

    //         let width = Math.floor((result.box.xMax - result.box.xMin) * canvas.width);
    //         let height = Math.floor((result.box.yMax - result.box.yMin) * canvas.height);
    //         let x = Math.floor(result.box.xMin * canvas.width);
    //         let y = Math.floor(result.box.yMin * canvas.height);
    
    //         x = x * scaleX;
    //         y = y * scaleY;
    //         width = width * scaleX;
    //         height = height * scaleY;
    
    //         ctx.beginPath();
    //         ctx.rect(x, y, width, height);
    //         ctx.lineWidth = 2;
    //         ctx.strokeStyle = 'red';
    //         ctx.fillStyle = 'red';
    //         ctx.stroke();
    //         ctx.fillText(result.label, x, y - 5);
    //     });
    // }    

    function drawBoundingBoxes(results) {
        // Clear previous bounding boxes
        const boundingBoxContainer = document.getElementById('boundingBoxContainer');
        boundingBoxContainer.innerHTML = '';

        // Draw bounding boxes based on the results received from the server
        results.forEach(result => {
            const boundingBox = document.createElement('div');
            const width = Math.floor((result.box.xMax - result.box.xMin) * canvas.width);
            const height = Math.floor((result.box.yMax - result.box.yMin) * canvas.height);
            const x = Math.floor(result.box.xMin * canvas.width);
            const y = Math.floor(result.box.yMin * canvas.height);
            boundingBox.className = 'bounding-box';
            boundingBox.style.position = 'absolute';
            boundingBox.style.left = `${x}px`;
            boundingBox.style.top = `${y}px`;
            boundingBox.style.width = `${width}px`;
            boundingBox.style.height = `${height}px`;
            const label = document.createElement('span');
            label.className = 'label';
            label.innerText = result.label;

            boundingBox.appendChild(label);
            boundingBoxContainer.appendChild(boundingBox);
        });
    }
});
