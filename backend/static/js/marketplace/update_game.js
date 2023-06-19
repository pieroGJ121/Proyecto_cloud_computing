let textarea = document.getElementById('synopsis')

textarea.addEventListener("input", autoResize, false);

const MAX_WORDS = 250;
const MAX_HEIGHT = 150;
function autoResize() {
  this.style.height = "auto";
  this.style.overflowY = "hidden";
  
  if (this.scrollHeight > MAX_HEIGHT) {
    this.style.height = MAX_HEIGHT + "px";
    this.style.overflowY = "auto";
  } else {
    this.style.height = this.scrollHeight + "px";
  }
  const words = textarea.value.trim().split(/\s+/);
  if (words.length >= MAX_WORDS) {
    textarea.value = words.slice(0, MAX_WORDS).join(' ');
    textarea.blur();
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
