window.onload = function() {
    set_information()
}

function set_information() {
    update_search("genre", "Todas")
    update_search("platform", "Todas")
    update_search("publisher", "Todas")
    update_search("name", "")

    set_list("genre")
    set_list("platform")
    set_list("publisher")
}

function set_list(categoria) {
    fetch(`/${categoria}`).then(function (response) {
        return response.json()
    }).then(function (elementos) {
        const list = document.getElementById(`list_${categoria}s`)

        elementos.forEach((elemento) => {
            const block = document.createElement("li")
            const classes = block.classList
            classs.add("sidenav-item")
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
