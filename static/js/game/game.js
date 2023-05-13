function comprar(event) {
    event.preventDefault();
  
    fetch('/verify_checkout',{
        method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        if (data.success === true) {
          window.location.href = '/checkout';
        } else {
          console.log('La verificación de compra no fue exitosa');
        }
      })
      .catch(error => {
        console.error('Error al realizar la verificación de compra:', error);
      });
  }
  