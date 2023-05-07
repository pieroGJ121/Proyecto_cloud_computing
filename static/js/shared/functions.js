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

function change_videogame() {
    fetch("/video_game").then(function (response) {
        return response.json()
    }).then(function (game_platform) {
        const platform = game_platform.platform
        const game_puplisher = game_platform.publisher
        const puplisher = game_publisher.publisher
        const game = game_publisher.game
        const genre = game.genre

        const game_name = document.getElementById("game_name")

        game_name.innerHTML = `${game.game_name}`

        const container_image = document.getElementByClassName("image_wide")[0]
        container_image.innerHTML = `
                        <img src="static/videogames/${game.image}">
                        `

        const synopsis = document.getElementById("synopsis")
        synopsis.innerHTML = `Sinopsis: ${game.synopsis}`

        const year = document.getElementById("year")
        year.innerHTML = `Año de lanzamiento: ${game_platform.release_year}`

        const genre = document.getElementById("genre")
        genre.innerHTML = `Sinopsis: ${game.genre.genre_name}`

        const publisher = document.getElementById("publisher")
        publisher.innerHTML = `Editor: ${publisher.publisher_name}`

        const platform = document.getElementById("platform")
        platform.innerHTML = `Plataforma: ${platform.platform_name}`
    })
}
