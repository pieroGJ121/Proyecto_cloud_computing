window.onload = function () {
    get_compra()
}

function get_compra () {
    fetch("/get_compra").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const compra = jsonResponse.compra
        const game = jsonResponse.game

        const name = document.getElementByClassName('title')
        name.innerHTML = game.game_name

        const purchase_date = document.getElementByClassName('purchase-date')
        purchase_date.innerHTML = `Fecha de compra: ${compra.created_at}`

        const id = document.getElementByClassName('order-id')
        id.innerHTML = `ID de compra: ${compra.id}`

        list_games(games_bought)
})}
