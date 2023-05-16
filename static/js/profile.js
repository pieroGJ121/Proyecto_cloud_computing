function change_profile() {
    fetch("/get_all_profile").then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        user = jsonResponse.user

        const name = document.getElementById("name")
        name.setAttribute("value", user.name)

        const lastname = document.getElementById("lastname")
        lastname.setAttribute("value", user.lastname)

        const bio = document.getElementById("bio")
        bio.innerHTML = user.bio

        const email = document.getElementById("email")
        email.setAttribute("value", user.email)

        const password = document.getElementById("password-field")
        password.setAttribute("value", user.password)
    })
}

window.onload = function() {
    change_profile()
}
