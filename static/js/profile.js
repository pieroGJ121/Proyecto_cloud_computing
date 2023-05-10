window.onload = function() {
    change_profile()
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
