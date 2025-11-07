window.addEventListener('load', () => {
    // پاک کردن داده‌های ذخیره‌شده در localStorage
    localStorage.removeItem('savedTutorials');
    // پاک کردن محتوای DOM
    const container = document.getElementById('savedTutorialsContainer');
    if (container) container.innerHTML = '';
});

document.addEventListener('DOMContentLoaded', () => {
    const videoTitleInput = document.getElementById('videoTitle');
    const tutorialPointsTextarea = document.getElementById('tutorialPoints');
    const saveButton = document.getElementById('saveButton');
    const captureFrameButton = document.getElementById('captureFrameButton');
    const savedTutorialsContainer = document.getElementById('savedTutorialsContainer');
    const capturedFramePreviewContainer = document.getElementById('capturedFramePreviewContainer');
    const savePdfButton = document.getElementById('savePdfButton'); // New: Get reference to Save PDF button

    const videoFileInput = document.getElementById('videoFileInput');
    const localVideoPlayer = document.getElementById('localVideoPlayer');
    const videoPlayerMessage = document.getElementById('videoPlayerMessage');

    let tutorials = JSON.parse(localStorage.getItem('tutorialVideos')) || [];

    // Clear input fields and preview container on page load
    videoTitleInput.value = '';
    tutorialPointsTextarea.value = '';
    capturedFramePreviewContainer.innerHTML = ''; // Clear any existing content

    function saveTutorialsToLocalStorage() {
        localStorage.setItem('tutorialVideos', JSON.stringify(tutorials));
    }

    // Helper to manage the "No frame captured yet" message in the preview container
    // This function will now only handle the initial message as the capture button no longer adds to this container.
    function updateCapturedFramesDisplay() {
        // If there are no immediate child elements (meaning no captured frames), add the empty message
        if (capturedFramePreviewContainer.children.length === 0 ||
            (capturedFramePreviewContainer.children.length === 1 && capturedFramePreviewContainer.querySelector('.empty-message'))) {
            // Check if message already exists to prevent duplicates
            if (!capturedFramePreviewContainer.querySelector('.empty-message')) {
                const emptyMessage = document.createElement('p');
                emptyMessage.textContent = 'No frame captured yet.';
                emptyMessage.classList.add('empty-message');
                capturedFramePreviewContainer.appendChild(emptyMessage);
            }
        } else {
            // If there are captured frames (from a previous implementation or other source), ensure the empty message is removed
            const emptyMessage = capturedFramePreviewContainer.querySelector('.empty-message');
            if (emptyMessage) {
                emptyMessage.remove();
            }
        }
    }

    function renderTutorials() {
        savedTutorialsContainer.innerHTML = '';

        if (tutorials.length === 0) {
            savedTutorialsContainer.innerHTML = '<p style="text-align: center; color: #666;">No tutorials saved yet. Start writing!</p>';
            return;
        }

        tutorials.forEach(tutorial => {
            const tutorialCard = document.createElement('div');
            tutorialCard.classList.add('tutorial-card');
            tutorialCard.setAttribute('data-id', tutorial.id);

            const titleElement = document.createElement('h3');
            titleElement.textContent = tutorial.title;

            const cardButtonsDiv = document.createElement('div');
            cardButtonsDiv.classList.add('card-buttons');

            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', () => {
                deleteTutorial(tutorial.id);
            });
            cardButtonsDiv.appendChild(deleteButton);

            tutorialCard.appendChild(titleElement);

            // Add image if available
            if (tutorial.image) {
                const imageElement = document.createElement('img');
                imageElement.src = tutorial.image;
                imageElement.alt = `Frame from ${tutorial.title}`;
                imageElement.classList.add('tutorial-thumbnail');
                tutorialCard.appendChild(imageElement);
            }

            // Add points if available (for regular tutorials or if image tutorials have points)
            if (tutorial.points) {
                const pointsElement = document.createElement('p');
                pointsElement.textContent = tutorial.points;
                tutorialCard.appendChild(pointsElement);
            }
            
            tutorialCard.appendChild(cardButtonsDiv);
            savedTutorialsContainer.appendChild(tutorialCard);
        });
    }


    function captureVideoFrame() {
        //if (!localVideoPlayer.src || localVideoPlayer.paused) {
        //    alert('Please load and play a video before capturing a frame.');
        //    return null;
        //}

        const canvas = document.createElement('canvas');
        // Ensure canvas dimensions match video for quality
        canvas.width = localVideoPlayer.videoWidth;
        canvas.height = localVideoPlayer.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(localVideoPlayer, 0, 0, canvas.width, canvas.height);

        return canvas.toDataURL('image/jpeg', 0.9); // Return as JPEG data URL with 90% quality
    }

    function addTutorial() {
        const title = videoTitleInput.value.trim();
        const points = tutorialPointsTextarea.value.trim();

        if (title === '' || points === '') {
            alert('Please enter both a video title and tutorial points.');
            return;
        }

        const newTutorial = {
            id: Date.now(),
            title: title,
            points: points
        };

        // Change: Add to the end of the tutorials array
        tutorials.push(newTutorial);
        saveTutorialsToLocalStorage();
        renderTutorials();

        videoTitleInput.value = '';
        tutorialPointsTextarea.value = '';
    }

    function deleteTutorial(id) {
        tutorials = tutorials.filter(tutorial => tutorial.id !== id);
        saveTutorialsToLocalStorage();
        renderTutorials();
    }

    videoFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileURL = URL.createObjectURL(file);
            localVideoPlayer.src = fileURL;
            localVideoPlayer.load();
            localVideoPlayer.play();
            videoPlayerMessage.textContent = `Playing: ${file.name}`;
        } else {
            localVideoPlayer.src = '';
            videoPlayerMessage.textContent = 'No video selected';
        }
    });

    captureFrameButton.addEventListener('click', () => {
        const frame = captureVideoFrame();
        if (frame) {
            // Stop video playing
            localVideoPlayer.pause();

            // Create a new tutorial object for the captured frame
            const newImageTutorial = {
                id: Date.now(),
                title: `Frame from video at ${new Date().toLocaleTimeString()}`, // Generated title
                points: '', // No specific points for a frame capture, leave empty
                image: frame // The captured image data URL
            };

            // Add this new tutorial to the end of the tutorials array
            tutorials.push(newImageTutorial);
            saveTutorialsToLocalStorage(); // Save updated tutorials array

            // Re-render all tutorials including the new image
            renderTutorials();

            // Clear the input fields after capturing a frame as a tutorial
            videoTitleInput.value = '';
            tutorialPointsTextarea.value = '';

            // The previous logic for adding to 'capturedFramePreviewContainer' is removed as per the requirements.
            // This button now adds the frame directly to 'savedTutorialsContainer'.
        }
    });

    saveButton.addEventListener('click', addTutorial);

    // New: Add event listener for the Save PDF button
    savePdfButton.addEventListener('click', () => {
        const element = savedTutorialsContainer;
        if (element.children.length === 1 && element.querySelector('p')) { // Check if only the "No tutorials saved yet" message is present
            alert('No tutorials to save. Please add some tutorials first.');
            return;
        }

        // Configure html2pdf options
        const options = {
            margin: 10,
            filename: 'tutorial_points.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        // Use html2pdf to generate and save the PDF
        html2pdf().set(options).from(element).save();
    });

    renderTutorials();
    updateCapturedFramesDisplay(); // Initialize preview area with "No frame captured yet"
});

document.getElementById('savePdfButton').addEventListener('click', () => {
    const container = document.getElementById('savedTutorialsContainer');

    if (!container || container.innerHTML.trim() === '') {
        alert('هیچ آموزشی برای ذخیره وجود ندارد.');
        return;
    }

    const opt = {
        margin:       0.5,
        filename:     'saved_tutorials.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(container).save();
});



