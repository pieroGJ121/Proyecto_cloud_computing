window.onload = function() {
    change_videogame()
}

function change_videogame() {
    fetch("/videogame").then(function (response) {
        return response.json()
    }).then(function (game_platform) {
        const platform_1 = game_platform.platform
        const game_puplisher = game_platform.publisher
        const puplisher = game_publisher.publisher
        const game = game_publisher.game
        const genre_1 = game.genre

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

        const genre_2 = document.getElementById("genre")
        genre.innerHTML = `Sinopsis: ${genre_1.genre_name}`

        const publisher = document.getElementById("publisher")
        publisher.innerHTML = `Editor: ${publisher.publisher_name}`

        const platform_2 = document.getElementById("platform")
        platform.innerHTML = `Plataforma: ${platform_1.platform_name}`
    })
}
