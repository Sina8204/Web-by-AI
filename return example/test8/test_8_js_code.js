document.addEventListener('DOMContentLoaded', () => {
    // Clear all previously stored comments from localStorage on page load
    document.querySelectorAll('.portfolio-item').forEach(item => {
        const projectId = item.dataset.projectId;
        localStorage.removeItem(`project-${projectId}-comments`);
    });

    // Function to load comments from localStorage for a specific project
    function loadComments(projectId) {
        const comments = JSON.parse(localStorage.getItem(`project-${projectId}-comments`)) || [];
        const commentsList = document.querySelector(`.portfolio-item[data-project-id="${projectId}"] .comments-list`);
        commentsList.innerHTML = ''; // Clear existing comments

        if (comments.length === 0) {
            const noCommentItem = document.createElement('li');
            noCommentItem.className = 'comment-item';
            noCommentItem.innerHTML = `<p>هنوز نظری ثبت نشده است.</p>`;
            commentsList.appendChild(noCommentItem);
            return;
        }

        comments.forEach(comment => {
            const listItem = document.createElement('li');
            listItem.className = 'comment-item';
            listItem.innerHTML = `
                <strong>${comment.name}</strong>
                <p>${comment.text}</p>
            `;
            commentsList.appendChild(listItem);
        });
    }

    // Function to save a new comment to localStorage
    function saveComment(projectId, comment) {
        const comments = JSON.parse(localStorage.getItem(`project-${projectId}-comments`)) || [];
        comments.push(comment);
        localStorage.setItem(`project-${projectId}-comments`, JSON.stringify(comments));
    }

    // Initialize comments and attach event listeners for all portfolio items
    document.querySelectorAll('.portfolio-item').forEach(item => {
        const projectId = item.dataset.projectId;
        loadComments(projectId); // Load comments when the page loads (will be empty after clearing)

        const form = item.querySelector('.comment-form');
        form.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent default form submission

            const nameInput = form.querySelector('.comment-name');
            const textInput = form.querySelector('.comment-text');

            if (!nameInput.value.trim() || !textInput.value.trim()) {
                alert('لطفاً نام و نظر خود را وارد کنید.');
                return;
            }

            const newComment = {
                name: nameInput.value.trim(),
                text: textInput.value.trim(),
                timestamp: new Date().toISOString() // Optional: add timestamp
            };

            // Save the new comment and reload the comments list for this project
            saveComment(projectId, newComment);
            loadComments(projectId);

            // Clear form fields after submission
            nameInput.value = '';
            textInput.value = '';
        });
    });

    // Optional: Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default anchor click behavior

            const targetId = this.getAttribute('href');
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth' // Smooth scroll to the target section
            });
        });
    });
});