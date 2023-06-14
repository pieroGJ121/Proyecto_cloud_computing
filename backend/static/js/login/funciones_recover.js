const pendingForms = new WeakMap()
const pendingForms2 = new WeakMap()
const data_recover = document.getElementById('data_recover')
const password_changer = document.getElementById('password_changer')
data_recover.addEventListener('submit', verify_submission)

function verify_submission(e){
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
  
    const formData = new FormData(formUserData)

    fetch('/data_recovery', {
        method: 'POST',
        body: formData,
    }).then(function (response) {
        return response.json()
      })
      .then(function (responseJson) {
        const message_error = document.getElementById('message_error')
        const password_changer = document.getElementById('password_changer')
        const submit1 = document.getElementById('submit1')
        const email = document.getElementById('email');
        const name = document.getElementById('name');
        const text_email = document.getElementById('text_email');
        const text_name = document.getElementById('text_name');
        const text_change = document.getElementById('text_change');

        if (!responseJson.success){
          message_error.style.display = 'block'
          password_changer.style.display = 'none'
          message_error.innerHTML = responseJson.message
          text_change.style.display = 'none'
        } 
        else{
            message_error.style.display = 'none'
            password_changer.style.display = 'block'
            submit1.style.display = 'none'
            text_change.style.display = 'block'
            email.disabled = true;
            name.disabled = true;
            text_email.innerHTML = ''
            text_name.innerHTML = ''
        }
      })
}

password_changer.addEventListener('submit', reset_password)

function reset_password(e){
    e.preventDefault()
    e.stopPropagation()
  
    //Handle abort previous request
    const formPassword = e.currentTarget
    const previousController = pendingForms2.get(formPassword)
    if (previousController) {
      previousController.abort()
    }
  
    const controller = new AbortController()
    pendingForms2.set(formPassword, controller)
    console.log('formCreateEmployee: ', formPassword)
  
    const formData = new FormData(formPassword)
    formData.append('email', data_recover.elements['email'].value);

    fetch('/password_recovery', {
        method: 'POST',
        body: formData,
    }).then(function (response) {
        return response.json()
      })
      .then(function (responseJson) {
        const message_error2 = document.getElementById('message_error2')

        if (!responseJson.success){
          message_error2.style.display = 'block'
          message_error2.innerHTML = responseJson.message
        } 
        else{
            message_error2.style.display = 'none'
            window.location.href = "/login";
        }
      })
}
