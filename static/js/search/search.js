document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault()  // Evita que el formulario se envíe de forma predeterminada

    const searchQuery = document.getElementById('SearchInput').value.trim()  // Obtiene el valor del campo de entrada y elimina los espacios en blanco al inicio y al final

    if (searchQuery.length > 0) {  // Verifica si el campo de entrada tiene al menos un carácter
        localStorage.setItem('searchQuery', searchQuery);
        const url = `/search`
        window.location.href = url
    }
});


