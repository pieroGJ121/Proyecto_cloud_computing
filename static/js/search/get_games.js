const searchQuery = localStorage.getItem('searchQuery');

window.addEventListener('load', () => {
    const search_text_p = document.getElementById('search_text_p')
    search_text_p.innerHTML = `Resultados de busqueda para: ${searchQuery}`
    get_games(searchQuery)
});

function get_games(searchQuery) {
    fetch(`/do_search/${searchQuery}`).then(respose => {
        return respose.json()
    }).then(jsonResponse => {
        const search_results_counter = document.getElementById('search_results_counter')
        if (jsonResponse.cantidad == 1) {
            search_results_counter.innerHTML = `Se ha encontrado ${jsonResponse.cantidad} resultado.`
            const container_games = document.getElementById('container_games');
            jsonResponse.juegos.forEach(juegos => {

                const cardDiv = document.createElement('a');
                cardDiv.classList.add('item_game');
                cardDiv.href = `/get_videogame/${juegos.id}`; // Reemplaza 'URL_DEL_JUEGO' con la URL real del juego
                
                const image = document.createElement('img');
                image.src = juegos.image;
                image.alt = 'Game_img';

                const title = document.createElement('h2');
                title.textContent = juegos.game_name;

                //const price = document.createElement('p');
                //price.textContent = `S/ 199`;

                cardDiv.appendChild(image);
                cardDiv.appendChild(title);
                //cardDiv.appendChild(price);
  
                container_games.appendChild(cardDiv);
            })

        }
        else if (jsonResponse.cantidad == 0){
            const container_games = document.getElementById('container_games')
            container_games.style.display = 'None'
            search_results_counter.innerHTML = `No se ha encontrado ningún resultado que coincida con la busqueda.`
        }
        else{
            search_results_counter.innerHTML = `Se han encontrado ${jsonResponse.cantidad} resultados.`
            const container_games = document.getElementById('container_games');
            jsonResponse.juegos.forEach(juegos => {

                const cardDiv = document.createElement('a');
                cardDiv.classList.add('item_game');
                cardDiv.href = `/get_videogame/${juegos.id}`; // Reemplaza 'URL_DEL_JUEGO' con la URL real del juego
                
                const image = document.createElement('img');
                image.src = juegos.image;
                image.alt = 'Game_img';

                const title = document.createElement('h2');
                title.textContent = juegos.game_name;

                //const price = document.createElement('p');
                //price.textContent = `S/ 199`;

                cardDiv.appendChild(image);
                cardDiv.appendChild(title);
                //cardDiv.appendChild(price);
  
                container_games.appendChild(cardDiv);
            })
        }
    })
}