function get_purchases () {
    const bought = document.getElementById('welcome_text')
    fetch("/get_compras").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        if (!jsonResponse.success) {
            fetch("/get_profile").then(function (response) {
                return response.json()
            }).then(function (data) {
                const user = data.user
                bought.innerHTML = `${user}, ${jsonResponse.message}`
                const counter_games = document.getElementById('counter_games')
                counter_games.style.display = 'none'
            })
        }
        else{
            fetch("/get_profile").then(function (response) {
                return response.json()
            }).then(function (data) {
                const user = data.user
                bought.innerHTML = `${user}, estos son los juegos que has comprado: `
            })

            const container_games = document.getElementById('container_games');

            jsonResponse.purchases.forEach(juego => {
                  // Crear el elemento div.item_game
                const itemGame = document.createElement('div');
                itemGame.classList.add('item_game');

                // Crear la imagen
                const imagen = document.createElement('img');
                imagen.src = juego.image;
                imagen.alt = juego.game_name;
                itemGame.appendChild(imagen);

                // Crear el título
                const titulo = document.createElement('h2');
                titulo.textContent = juego.game_name;
                itemGame.appendChild(titulo);

                // Crear el precio
                const precio = document.createElement('p');
                precio.textContent = `S/ 199 (No oficial)`;
                itemGame.appendChild(precio);

                // Crear la fecha de compra
                const fechaCompra = document.createElement('p');
                fechaCompra.textContent = `Fecha de compra: ${juego.fecha_compra}`;
                itemGame.appendChild(fechaCompra);

                // Agregar el elemento al contenedor
                container_games.appendChild(itemGame);
            });

            const counter_games = document.getElementById('counter_games')
            counter_games.innerHTML = `En total has adquirido ${jsonResponse.purchases.length} juegos`
        }
    })
}





document.addEventListener('DOMContentLoaded', function(){
    get_purchases()
})