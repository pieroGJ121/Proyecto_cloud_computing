function list_games(games) {
    const container_games = document.getElementById("container_games")
    const search_text_p = document.getElementById('search_text_p')
    if (games.length == 0) {
        search_text_p.innerHTML = "No hay resultados que coincidan con la busqueda"
        container_games.innerHTML = ''
        const search_results_counter = document.getElementById('search_results_counter')
        search_results_counter.style.display = 'None'
    } else {
        search_text_p.innerHTML = "Resultados para la busqueda: "
        container_games.innerHTML = ""
        games.forEach((game) => {
            const block = document.createElement("div")
            block.classList.add("item_game")
            block.setAttribute("id", game.id)
            block.setAttribute("onclick", `go_to_videogame(${game.id})`)

            block.innerHTML = `
                    <img src="${game.image}">
                    <h4>${game.game_name}</h4>
                    <p>${game.synopsis}</div>
                    `
            container_games.appendChild(block)
        })
    }
}

function go_to_videogame(id) {
    const params = new URLSearchParams()
    params.append("id", id)
    const url = "/videogame?" + params.toString()
    window.location.href = url
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
        .then(function (response) {
            return response.json()
        }).then(function (jsonResponse) {
            games = jsonResponse.games
            list_games(games)
        })
}


function do_search(name) {
    if (window.location.pathname != "/search") {
        const params = new URLSearchParams()
        params.append("genre", "Todas")
        params.append("platform", "Todas")
        params.append("publisher", "Todas")
        params.append("name", name)
        const url = "/search?" + params.toString()
        window.location.href = url
    } else {
        update_search_params("name", name)
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const formulario = document.getElementById('searchForm');
    formulario.addEventListener('submit', function(event) {
        event.preventDefault()
        const campoBusqueda = formulario.elements['SearchInput'].value;
        do_search(campoBusqueda)
    })
})
