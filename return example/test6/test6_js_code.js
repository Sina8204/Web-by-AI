document.addEventListener('DOMContentLoaded', () => {
    const selectVideoButton = document.getElementById('selectVideoButton');
    const videoFileInput = document.getElementById('videoFileInput');

    let currentVideoObjectURL = null; // To keep track of the object URL for revoking

    // Function to revoke the current object URL
    const revokeCurrentObjectURL = () => {
        if (currentVideoObjectURL) {
            URL.revokeObjectURL(currentVideoObjectURL);
            currentVideoObjectURL = null;
        }
    };

    // Revoke URL when the main page unloads
    window.addEventListener('beforeunload', revokeCurrentObjectURL);

    // Trigger the hidden file input when the button is clicked
    selectVideoButton.addEventListener('click', () => {
        videoFileInput.click();
    });

    // Handle file selection
    videoFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0]; // Get the first selected file

        if (file) {
            // Check if the file is a video
            if (file.type.startsWith('video/')) {
                // Revoke any previously created object URL
                revokeCurrentObjectURL();

                // Create a URL for the selected file
                const videoURL = URL.createObjectURL(file);
                currentVideoObjectURL = videoURL; // Store for future revoking

                // Open a new window/tab
                const newWindow = window.open('', '_blank');

                if (newWindow) {
                    newWindow.document.write(`
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Playing Video</title>
                            <style>
                                body { margin: 0; background-color: #000; overflow: hidden; }
                                video { display: block; width: 100vw; height: 100vh; object-fit: contain; }
                            </style>
                        </head>
                        <body>
                            <video controls autoplay src="${videoURL}"></video>
                        </body>
                        </html>
                    `);
                    newWindow.document.close();
                } else {
                    alert('Popup blocked! Please allow popups for this site to play video in a new tab.');
                    revokeCurrentObjectURL(); // If popup is blocked, revoke immediately
                }
            } else {
                alert('Please select a valid video file.');
                revokeCurrentObjectURL(); // Clear any previous URL if invalid file selected
            }
        }
        // Clear the file input value so that selecting the same file again triggers the 'change' event
        videoFileInput.value = '';
    });
});