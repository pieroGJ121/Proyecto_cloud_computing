const pendingForms = new WeakMap()
const login_data = document.getElementById('login_data')
login_data.addEventListener('submit', verify_login)

function verify_login(e){
    e.preventDefault()
    e.stopPropagation()
  
    //Handle abort previous request
    const formLogin = e.currentTarget
    const previousController = pendingForms.get(formLogin)
    if (previousController) {
      previousController.abort()
    }
  
    const controller = new AbortController()
    pendingForms.set(formLogin, controller)
    console.log('formCreateEmployee: ', formLogin)
  
    const formData = new FormData(formLogin)

    fetch('/data_login', {
        method: 'POST',
        body: formData,
    }).then(function (response) {
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

