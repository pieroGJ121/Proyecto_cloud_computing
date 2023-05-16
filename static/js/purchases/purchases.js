function get_purchased_games () {
    fetch("/get_purchased_games").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const user = jsonResponse.user
        const games_bought = jsonResponse.games

        const bought = document.getElementById('welcome_text')
        bought.innerHTML = `${user.name}, estos son los juegos que has comprado:`

        const counter_games = document.getElementById('counter_games')
        counter_games.innerHTML = `En total has adquirido ${games_bought.length} juegos`

        const container_games = document.getElementById("container_games")
        container_games.innerHTML = ""

        list_games(games_bought, "Fecha de Compra: ", "bought_at", container_games)
})}

window.onload = function () {
    get_purchased_games()
}
