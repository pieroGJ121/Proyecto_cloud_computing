function update_search_params(categoria, elemento) {
    let url = new URL(window.location)
    url.searchParams.set(categoria, elemento)

    url.search = url.searchParams
    url = url.toString()

    history.pushState({}, null, url)

    fetch(`/search`)
        .then(function (response) {
            return response.json()
        }).then(function (games) {
            list_games(games)
        })
}
