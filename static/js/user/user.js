function hide_msg() {
    const confirm_msg = document.getElementById('confirm_msg')
    const submit_final = document.getElementById('submit_final')
    const prev_submit = document.getElementById('prev_submit')

    confirm_msg.style.display = 'Block'
    prev_submit.style.display = 'None'
    submit_final.style.display = 'Block'
}
function delete_user(){
    fetch('/delete_user', {
        method: 'POST',
    })
    .then(function (response) {
        console.log('response', response)
        return response.json()
      })
    .then(function (responseJson) {
        if (!responseJson.success){
          const message_error = document.getElementById('message_error')
          message_error.style.display = 'block'
          message_error.innerHTML = responseJson.message
        } 
        else{
            message_error.style.display = 'none'
            window.location.href = "/";
        }
      })
}


const MAX_WORDS = 50; // Define el número máximo de palabras permitido
const textarea = document.querySelector('textarea');

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