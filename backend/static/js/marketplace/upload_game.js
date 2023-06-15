let textarea = document.getElementById('synopsis')

textarea.addEventListener("input", autoResize, false);

const MAX_WORDS = 250; // Define el número máximo de palabras permitido
const MAX_HEIGHT = 150;
function autoResize() {
  this.style.height = "auto";
  this.style.overflowY = "hidden"; // Inicialmente oculta el scrollbar vertical
  
  if (this.scrollHeight > MAX_HEIGHT) {
    this.style.height = MAX_HEIGHT + "px"; // Establece la altura máxima
    this.style.overflowY = "auto"; // Activa el scrollbar vertical
  } else {
    this.style.height = this.scrollHeight + "px";
  }
  const words = textarea.value.trim().split(/\s+/); // Divide el contenido del textarea en palabras
  if (words.length >= MAX_WORDS) { // Corregido: utiliza "words.length >= MAX_WORDS"
    textarea.value = words.slice(0, MAX_WORDS).join(' '); // Si se supera el límite de palabras, se borra lo que se escriba extra
    textarea.blur(); // Desactiva la edición del textarea
  }
}

document.getElementById('upload_button').addEventListener('click', function() {
  document.getElementById('image_upload').click();
});


const input = document.getElementById('image_upload');
const preview = document.getElementById('preview-image');


input.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    const prev = document.getElementById('prev');
    prev.style.display = 'none';

    const extension = file.name.split('.').pop();
    if (extension != 'jpg' && extension != 'jpeg' && extension != 'png') {
      preview.src = 'https://cdn-icons-png.flaticon.com/512/1602/1602722.png';
    } else {
      preview.src = e.target.result;
    }
  };

  reader.readAsDataURL(file);
});
