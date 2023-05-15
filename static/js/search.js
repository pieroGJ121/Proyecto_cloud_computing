function set_information() {
    set_list("genre", "1-0-0")
    set_list("platform", "1-0-1")
    set_list("publisher", "1-0-2")

    update_search_params("genre", "Todas")
}

function set_list(categoria, list_id) {
    fetch(`/get_${categoria}`).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        const elementos = jsonResponse.elementos

        const list = document.getElementById(`sidenav-collapse-${list_id}`)

        elementos.forEach((elemento) => {
            const block = document.createElement("li")
            const classes = block.classList
            classes.add("sidenav-item")
            block.id = `${elemento.name}`
            block.setAttribute("onclick", `update_search_params("${categoria}", "${elemento.name}")`)

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
