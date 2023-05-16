window.onload = function () {
    get_purchases()
}

function get_purchases () {
    fetch("/get_profile").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const user = jsonResponse.user
        const games_bought = user.games_bought

        const bought = document.getElementById('welcome_text')
        bought.innerHTML = `${user.name}, estos son los juegos que has comprado:`

        const counter_games = document.getElementById('counter_games')
        counter_games.innerHTML = `En total has adquirido ${games_bought.length} juegos`

        list_games(games_bought)
})}
