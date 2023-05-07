function list_games(games) {
    const list_games = document.getElementByClassName("list_games")[0]
    if (games.length == 0) {
        list_games.innerHTML = "There are no games"
    } else {
        list_games.innerHTML = ""
        games.forEach((game) => {
            const block = document.createElement("div")

            block.innerHTML = `
                    <div class="image_wide">
                        <img src="static/videogames/${game.image}">
                    </div>
                    <div class="game_basic_info">
                        <h4>${game.game_name}</h4>
                        <div>${game.synopsis}</div>
                    </div>
                    `
            list_games.appendChild(block)
        })
    }
}

function change_profile() {
    fetch("/profile").then(function (response) {
        return response.json()
    }).then(function (user) {
        const name = document.getElementById("name")
        name.innerHTML = `Nombre: ${user.firstname} ${user.lastname}`

        const email = document.getElementById("email")
        email.innerHTML = `Correo electrónico: ${user.email}`

        const bio = document.getElementById("bio")
        email.innerHTML = `Bio: ${user.bio}`

        list_games(user.games_bought)
    })
}
