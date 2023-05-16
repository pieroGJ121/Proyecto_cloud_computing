function get_compra () {
    const id_game = localStorage.getItem('id_game');
    fetch(`/add_compra/${id_game}`, {
        method: 'POST',
    }).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const compra = jsonResponse.compra
        const game = compra.game

        const title = document.getElementById('titulo_principal')
        title.innerHTML = `Gracias por comprar ${game.game_name}`

        const game_title = document.getElementById('game_title')
        game_title.innerHTML = `${game.game_name}`

        const container_image = document.getElementById('game_image')
        container_image.innerHTML = `
                        <img src="${game.image}" alt="Game Image">
                        `
        const purchase_date = document.getElementById('purchase_date')
        purchase_date.innerHTML = `Fecha de compra: ${compra.created_at}`

        const id = document.getElementById('order_id')
        id.innerHTML = `ID de compra: ${compra.id}`

})}

document.addEventListener('DOMContentLoaded', function() {
    get_compra()
});
