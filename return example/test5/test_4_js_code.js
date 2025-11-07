document.addEventListener('DOMContentLoaded', () => {
    const openFileButton = document.getElementById('openFileButton');
    const imageInput = document.getElementById('imageInput');
    const displayImage = document.getElementById('displayImage');
    const imagePlaceholder = document.getElementById('imagePlaceholder');

    openFileButton.addEventListener('click', () => {
        imageInput.click(); // Trigger the hidden file input click
    });

    imageInput.addEventListener('change', (event) => {
        const file = event.target.files[0]; // Get the selected file

        if (file) {
            const reader = new FileReader(); // Create a FileReader object

            reader.onload = (e) => {
                // When the file is loaded, set the image source
                displayImage.src = e.target.result;
                displayImage.style.display = 'block'; // Show the image
                imagePlaceholder.style.display = 'none'; // Hide the placeholder text
            };

            reader.readAsDataURL(file); // Read the file as a data URL
        } else {
            // No file selected or selection was cancelled
            displayImage.src = '';
            displayImage.style.display = 'none'; // Hide the image
            imagePlaceholder.style.display = 'block'; // Show the placeholder text
        }
    });
});