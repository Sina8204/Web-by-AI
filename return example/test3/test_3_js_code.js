document.addEventListener('DOMContentLoaded', () => {
    const createButton = document.getElementById('createButton');
    const buttonContainer = document.getElementById('buttonContainer');
    let buttonCount = 0;

    createButton.addEventListener('click', () => {
        buttonCount++;
        const newButton = document.createElement('button');
        newButton.classList.add('dynamic-button');
        newButton.textContent = `Button ${buttonCount}`;
        buttonContainer.appendChild(newButton);
    });
});