const MAX_WORDS = 50; // Define el número máximo de palabras permitido
const textarea = document.querySelector('textarea');
const pendingForms = new WeakMap()
const register_data = document.getElementById('register_data')
register_data.addEventListener('submit', register)

function register(e){
    e.preventDefault()
    e.stopPropagation()
  
    //Handle abort previous request
    const formUserData = e.currentTarget
    const previousController = pendingForms.get(formUserData)
    if (previousController) {
      previousController.abort()
    }
  
    const controller = new AbortController()
    pendingForms.set(formUserData, controller)
    console.log('formCreateEmployee: ', formUserData)
  
    const formData = new FormData(formUserData)

    fetch('/new_user', {
        method: 'POST',
        body: formData,
    }).then(function (response) {
        console.log('response', response)
        return response.json()
      })
      .then(function (responseJson) {
        const message_error = document.getElementById('message_error')

        if (!responseJson.success){
          message_error.style.display = 'block'
          message_error.innerHTML = responseJson.message
        } 
        else{
          message_error.style.display = 'none'
          window.location.href = "/";
        }
      })
}

var autosizeScript = document.createElement('script');
autosizeScript.src = "https://cdnjs.cloudflare.com/ajax/libs/autosize.js/4.0.2/autosize.min.js";
document.head.appendChild(autosizeScript);

// Espera a que la biblioteca Autosize se cargue y, a continuación, inicializa el texto
autosizeScript.onload = function() {
  autosize(document.querySelector('textarea'));
}

// Agrega un listener para el evento input en el textarea
textarea.addEventListener('input', () => {
  const words = textarea.value.trim().split(/\s+/); // Divide el contenido del textarea en palabras
  if (words.length > MAX_WORDS) {
    textarea.value = words.slice(0, MAX_WORDS).join(' '); // Si se supera el límite de palabras, se borra lo que se escriba extra
    textarea.blur(); // Desactiva la edición del textarea
  }
});
