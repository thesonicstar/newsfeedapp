document.getElementById('fetch-news').addEventListener('click', () => {
    const category = document.getElementById('category').value;
    fetch(`/get_news?category=${category}`)
        .then(response => response.json())
        .then(data => {
            const newsContainer = document.getElementById('news-container');
            newsContainer.innerHTML = ''; // Clear previous results
            data.articles.forEach(article => {
                const articleDiv = document.createElement('div');
                articleDiv.className = 'article';
                articleDiv.innerHTML = `
                    <h2>${article.title}</h2>
                    <p>${article.description}</p>
                    <a href="${article.url}" target="_blank">Read more</a>
                `;
                newsContainer.appendChild(articleDiv);
            });
        });
});
