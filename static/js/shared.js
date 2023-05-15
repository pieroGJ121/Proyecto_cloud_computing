function list_games(games) {
    const container_games = document.getElementByClassName("container_games")[0]
    if (games.length == 0) {
        container_games.innerHTML = "There are no games"
    } else {
        container_games.innerHTML = ""
        games.forEach((game) => {
            const block = document.createElement("div")
            block.classList.add("item_game")
            block.setAttribute("id", game.id)

            block.innerHTML = `
                    <img src="${game.image}">
                    <h4>${game.game_name}</h4>
                    <p>${game.synopsis}</div>
                    `
            container_games.appendChild(block)
        })
    }
}

// Obtener todos los elementos con la clase "item_game"
var itemGames = document.getElementsByClassName('item_game');

// Iterar sobre los elementos y agregar el evento de clic a cada uno
for (var i = 0; i < itemGames.length; i++) {
  itemGames[i].addEventListener('click', function() {
    window.location.href = '/videogame';
    update_search_params('id', this.getAttribute('id'));
  });
}

function change_search_params(categoria, elemento) {
    let url = new URL(window.location)
    url.searchParams.set(categoria, elemento)

    url.search = url.searchParams
    url = url.toString()

    history.pushState({}, null, url)

}

function update_search_params(categoria, elemento) {
    change_search_params(categoria, elemento)

    const params = new URLSearchParams(window.location.search)
    const url = "/do_search?" + params.toString()
    let games

    fetch(url)
    // The do_search endpoint doesn't have the query parameters, only search does
        .then(function (response) {
            return response.json()
        }).then(function (jsonResponse) {
            console.log(jsonResponse)
            games = jsonResponse.games
        })
    list_games(games)
}


function do_search(name) {
    if (window.location.pathname != "/search") {
        window.location.pathname = "/search"
    }
    update_search_params("name", name)
}

document.addEventListener('DOMContentLoaded', function(){
    const formulario = document.getElementById('searchForm');
    formulario.addEventListener('submit', function(event) {
        event.preventDefault()
        const campoBusqueda = formulario.elements['SearchInput'].value;
        console.log(campoBusqueda)
        do_search(campoBusqueda)
    })
})
