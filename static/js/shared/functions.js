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
