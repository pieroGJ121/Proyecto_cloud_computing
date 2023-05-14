function set_information(name) {
    update_search_params("genre", "Todas")
    update_search_params("platform", "Todas")
    update_search_params("publisher", "Todas")

    set_list("genre")
    set_list("platform")
    set_list("publisher")
}

function set_list(categoria) {
    fetch(`/get_${categoria}`).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const elementos = jsonResponse.elementos

        const list = document.getElementById(`list_${categoria}s`)

        elementos.forEach((elemento) => {
            const block = document.createElement("li")
            const classes = block.classList
            classes.add("sidenav-item")
            block.id = `${elemento.name}`
            block.onclick = update_search_params(categoria, elemento.name)

            block.innerHTML = `
                    <a class="sidenav-link">${elemento.name}</a>
                    `

            list.appendChild(block)
        })

    })
}

window.onload = function() {
    set_information()
}
