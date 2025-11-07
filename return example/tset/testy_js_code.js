document.addEventListener('DOMContentLoaded', () => {
    console.log('Weblog loaded!');

    const blogPostsContainer = document.getElementById('blog-posts');

    // Dynamically add a new blog post using JavaScript
    const newPostData = {
        title: 'Exploring Web Development Basics',
        date: 'October 28, 2023',
        author: 'John Doe',
        content: `
            <p>Today, I've been diving into the fundamentals of web development, specifically HTML, CSS, and JavaScript. It's fascinating how these three technologies work together to create interactive and beautiful websites.</p>
            <p>HTML provides the structure, CSS adds the style, and JavaScript brings the interactivity. Each component is essential, and understanding their synergy is key to building robust web applications.</p>
            <p>I'm particularly enjoying experimenting with CSS Grid and Flexbox for layout. They offer so much power and flexibility!</p>
        `
    };

    const newArticle = document.createElement('article');
    newArticle.classList.add('blog-post');

    // Using innerHTML to set the content for simplicity in this example
    newArticle.innerHTML = `
        <h2>${newPostData.title}</h2>
        <div class="post-meta">
            <span class="post-date">${newPostData.date}</span> by
            <span class="post-author">${newPostData.author}</span>
        </div>
        <div class="post-content">
            ${newPostData.content}
        </div>
    `;

    blogPostsContainer.appendChild(newArticle);

    console.log('A new post has been added dynamically!');
});