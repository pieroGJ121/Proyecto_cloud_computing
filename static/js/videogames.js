function change_videogame() {
    const url = window.location.href;
    const urlObj = new URL(url);
    const searchParams = new URLSearchParams(urlObj.search);
    const identificador = searchParams.get("id");

    fetch(`/get_videogame/${identificador}`).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        console.log(jsonResponse)
        const game_platform = jsonResponse.game_platform
        //const platform_game = game_platform.platform

        //const platform = game_platform.platform
        const game_publisher = game_platform.game_publisher
        const puplisher = game_publisher.publisher
        const game = game_publisher.game
        const genre_game = game.genre

        const title = document.getElementById('titulo_principal')
        title.innerHTML = `${game.game_name}`
        
        const game_name = document.getElementById("game_name")
        game_name.innerHTML = `${game.game_name}`
        
        const container_image = document.getElementById("game_image")
        container_image.innerHTML = `
                        <img src="${game.image}" alt="Game Image">
                        `
        
        const synopsis_p = document.getElementById("synopsis_p")
        synopsis_p.innerHTML = `${game.synopsis}`
        
        const year = document.getElementById("year")
        year.innerHTML = `Año de lanzamiento: ${game_platform.release_year}`
        
        const genre_tag = document.getElementById("genre")
        genre_tag.innerHTML = `Género: ${genre_game.name}`

        const publisher = document.getElementById("publisher")
        publisher.innerHTML = `Editor: ${puplisher.name}`

        const platform_tag = document.getElementById("platform")
        platform_tag.innerHTML = `Plataforma(s): ${game_platform.platform.name}`
    })
}


function change_buy_button() {
    const url = window.location.href;
    const urlObj = new URL(url);
    const searchParams = new URLSearchParams(urlObj.search);
    const identificador = searchParams.get("id");
    
    fetch(`/is_game_bought/${identificador}`).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        console.log(jsonResponse)
        
        const buy_button = document.getElementById("buy_button")
        if (jsonResponse.is_bought == 1) {
            buy_button.innerHTML = "Juego comprado"
        } else {
            buy_button.innerHTML = "Comprar ahora"
        }
    })
}
/*
function comprar(event) {
    event.preventDefault();
    const buy_message = document.getElementById("buy_message")
    let url = new URLSearchParams(document.location.search)
    let id_game = params.get("id")

    fetch("/is_game_bought").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        if (jsonResponse.is_bought == 1) {
            buy_message.innerHTML = "Ya has comprado este juego"
        } else {
            fetch('/buy_game', {
                method: 'POST',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success === true) {
                        window.location.href = '/checkout';
                        update_search_params("id", id_game)
                    } else {
                        buy_message.innerHTML = 'La verificación de compra no fue exitosa'
                        setTimeout(function() {
                            buy_message.innerHTML = ''
                        }, 5000);
                    }
                })
                .catch(error => {
                    buy_message.innerHTML = 'Error al realizar la verificación de compra:'
                        setTimeout(function() {
                            buy_message.innerHTML = ''
                        }, 5000);
                });
        }
    })
}

*/

document.addEventListener('DOMContentLoaded', function() {
    change_videogame();
    change_buy_button();
});

