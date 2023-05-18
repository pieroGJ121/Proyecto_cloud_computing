<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/CS1103/proyecto-final-2023_0-proyecto-final-2023_0-grupo-5">
    <img src="static/logo/logo_2.png" alt="hex board" width="300" height="100">
  </a>
  <h1>👾 GPT VIDEOGAMES 👾</h1>
  
  <p>
  Este proyecto ha sido desarrollado por estudiantes del curso de Desarrollo Basado en Plataformas
de la Universidad de Ingeniería y Tecnología 💙🤍. Esperemos les guste. 🎮
    
  </p>
</div>

<details open>
  <summary>Índice:</summary>
  <ol>
    <li><a href="#integrantes">
      Integrantes
    </a></li>
    <li><a href="#acerca-del-proyecto">
      Acerca del proyecto
      <ul>
        <li><a href="#descripción">Descripción</a></li>
        <li><a href="#objetivos-principales">Objetivos Principales</a></li>
        <li><a href="#librerías-framworks-y-plugins">Librerías, Frameworks y Plugins</a></li>
        <li><a href="#script">Script</a></li>
        <li><a href="#rutas">Rutas</a></li>
        <li><a href="#hosts">Hosts</a></li>
        <li><a href="#manejo-de-errores-http">Manejo de Errores HTTP</a></li>
        <li><a href="#ejecución-del-sistema">Ejecución del Sistema</a></li>
      </ul>
    </a></li>
  </ol>
</details>

---

## Integrantes

- Piero Jesus Guerrero Jimenez				
- Fabrizzio Nicolay Vilchez Espinoza				
- Manuel Jesus Silva 				
- Ariana Vega Huamán				 

## Acerca del proyecto

### Descripción

Este proyecto consiste en el desarrollo de una aplicación virtual llamada GPT VIDEOGAMES,
la cual consiste en vender videojuegos de manera virtual, ya sea por marcas, plataformas o categorías.

### Objetivos Principales

#### Misión

Esta página tiene como misión llegar a ser de total comodidad para el cliente y cumplirlo ofreciendo videojuegos de alta calidad.

#### Visión

La visión de esta página es ser una de las plataformas líderes en la industria de entretenimiento electrónico y afines en el Perú.

### Librerías, Frameworks y Plugins

Front-end:
- Bootstrap: Bootstrap es un framework de desarrollo web gratuito y de código abierto. Está diseñado para facilitar el proceso de desarrollo de los sitios web responsivos y orientados a los dispositivos móviles, proporcionando una colección de sintaxis para diseños de plantillas.

Back-end:
- Flask: Flask es un framework ligero de desarrollo web en Python que permite crear aplicaciones web rápidas y eficientes. Proporciona herramientas y bibliotecas para manejar solicitudes HTTP, enrutar URL, generar respuestas dinámicas y gestionar bases de datos. Flask es altamente personalizable y fácil de aprender, lo que lo convierte en una elección popular para desarrolladores de backend. Se usa en este proyecto para manejar las solicitudes a la base de datos y algunas operaciones de verificación.

- SQLAlchemy: SQLAlchemy es una biblioteca de mapeo objeto-relacional en Python que facilita la interacción con bases de datos relacionales. Proporciona una capa de abstracción que permite interactuar con la base de datos utilizando objetos y consultas en lugar de escribir consultas SQL directamente. SQLAlchemy simplifica el manejo de la persistencia de datos y la creación de consultas complejas.
- SMTPLIB: La biblioteca smtplib de Python se utiliza para enviar correos electrónicos a través de un servidor SMTP. Primero, se establece una conexión con el servidor utilizando smtplib.SMTP, luego se autentica con credenciales y se envía el correo utilizando sendmail. Todo esto se usa para enviar correos al usuario al final de la compra.

Base de Datos:
- Flask_migrate
- SQLAlchemy

### Script

Para cargar las bases de datos se ejecuta:
```sh
./load.sh
```
- Se debe estar dentro del repositorio, en el mismo nivel que app.py.
- Dentro del script, primero se ejecuta python app.py, para crear las bases de datos. -
- Luego de cargar, se debe cancelar con Ctr+c.
- Después, se usa ejecuta el código de los sql scripts encontrados dentro de la carpete /sql. Estos llenan las tablas de la base de datos con los datos de los videojuegos.

### Rutas

- @app.route('/', methods=['GET'])
  Esta ruta se ejecuta para poder ingresar a la aplicación.
  - En caso de que se loguee, se renderiza a la vista index
  - En caso de que no esté logueado, se redirecciona a la ruta login

- @app.route('/login', methods=['GET'])
  Si ya está logueado, te va a redirigir a la vista principal
  Y en caso no lo esté, te renderiza a la vista login.

- @app.route('/data_login', methods=['POST'])
  Esta ruta sirve para validad de que el ususario esté logueado.
  - Primero va a requrir el correo y la contraseña del usuario. 
  - Se busca el primer usuario que coincida con el email puesto en el formulario
  - De ahí, si el usuario existe y es correcto, retorna un mensaje de inicio de sesión correcto.
  - Si el ususario en incorrecto, retorna un mensaje de correo y/o contraseña incorrectos.
  - Y, si es que el ususario no existe, te retorna un mensaje de ususario no registrado.

- @app.route('/logout', methods=['GET'])
  Esta ruta sirve para cerrar sesión y te redirige a la página de login.
  
- @app.route('/password_recovery', methods=['GET'])
  Esta ruta sirve para cambiar de contraseña.
  
- @app.route('/data_recovery', methods=['POST'])
  Esta ruta sirve para recuperar datos.
  - Primero pones los datos que quieres recuperar en el formulario (nombre e email)
  - De ahí, se buscan en la base de datos:
   - Si coinciden, te manda el mensaje de que todo coincide
   - Si no coinciden, te manda el mensaje de intentar de nuevo
   - Y si el ususario no existe, te manda el mensaje que no hay ususario registrado

- @app.route('/password_change', methods=['POST'])
  Esta ruta sirve para reestablecer la contraseña
  - Primero te pide que ingreses la contraseña nueva y la vuelvas a escribir en otro cambio
   - Si las contraseñas coinciden, te manda un mensaje de cambio exitoso
   - Si no coinciden, te manda una mensaje indicando que no coinciden

- @app.route('/new_user', methods=['GET'])
  Esta ruta sirve para agregar un nuevo ususario y te renderiza a la vista register

- @app.route('/new_user', methods=['POST'])
  Esta ruta sirve para agregar la info del nuevo usuario a registrar
  Te pide completar los campos del formulario y valida el correo
   - Si el correo ya existe en la base de datos, te retornará un mensaje de correo ya registrado
   - Si el correo no se encuentra en la base de datos, se registrará y te retornará un mensaje de correo valido
  En caso de que el email no sea validado, te retornará un mensaje de correo no valido
  
- @app.route('/profile', methods=['GET'])
  Esta ruta sirve para ingresar a tu perfil
  - Si estas logueado y todo es corrercto, te va a renderizar a la vista user
  - Si no está logueado, te va a redirigir a la página principal
 
- @app.route('/profile_data', methods=['GET'])
  Esta ruta sirve para validar los datos correspondientes al email ingresado.
  
- @app.route('/user_deletion', methods=['POST'])
  Esta ruta sirve para eliminar el usuario
  - Primero, para poder eliminar el usuario, se tienen que eliminar las compras realizadas por este
  - Después, se busca en la base de datos aquellas compras relacionadas con el id del usuario y se eliminan
  - De ahí, se actualiza la base de datos y se eliminan esos datos
   - Si se eliminaron los datos correctamente, te retornará que el ususario fue eliminado exitosamente
   - Si no se pudo, retornará que lo intentes nuevamente
 
- @app.route('/data_modification', methods=['POST'])
  Esta ruta sirve para actualizar los datos del usuario
  - Te pide rellenar el formulario con los nuevos datos
  - De ahí, buscas al ususario y actualizas los campos
  - y te redirecciona a la página principal

- @app.route('/videogame_data/<identificador>', methods=['GET'])
  Esta ruta sirve para obtener los datos del videojuego en base a su id.
  
- @app.route('/videogame', methods=['GET'])  
  Esta ruta sirve para obtener la lista de videojuegos.

- @app.route('/genre_data', methods=['GET'])
  Esta ruta sirve para obtener todos los géneros de videojuegos
  
- @app.route('/platform_data', methods=['GET'])
  Esta ruta sirve para obtener todas las plataformas de videojuegos
  
- @app.route('/publisher_data', methods=['GET'])
  Esta ruta sirve para obtener todas
  
- @app.route('/search_query', methods=['GET'])
  Esta ruta sirve hacer una búsqueda mediante filtros
  - Primero hace la consulta a base de las 4 opciones (videojuego, género, plataforma o publisher)
  - Luego filtra a los videojuegos que cumplan con el requerimiento seleccionado
  
- @app.route('/search', methods=['GET'])
  Esta ruta sirve para validar que esté logueado
  - Si está logueado, te renderiza a la vista "search"
  - Si no está logueado, te redirige a la página principal
  
- @app.route('/purchases', methods=['GET'])
  Esta ruta sirve para validar que esté logueado
  - Si está logueado, te renderiza a la vista "purchase"
  - Si no está logueado, te redirige a la página principal
  
- @app.route('/games_purchased', methods=['GET'])
  Esta ruta busca al usuario y te retorna las compras que ha realizado.
  
- @app.route('/compra_data/<identificador>', methods=['GET'])  
  Esta ruta sirve para obtener los datos de todas las compras que hizo el usuario.
  
- @app.route('/new_compra/<identificador>', methods=['POST'])   
  Esta ruta sirve para validar y crear una nueva compra 
  - Cuando está validado toda la info requerida, te envía un correo confirmando la compra realizada
  
- @app.route('/game_state/<identificador>', methods=['GET'])
  Esta ruta sirve para vel el estado de tu compra
  
- @app.route('/new_game', methods=['POST'])
  Esta ruta sirve para agregar un nuevo juego al carrito de compras.
  
- @app.route('/checkout', methods=['GET'])
  Esta ruta sirve para verificar la compra
  - Si la compra no está verificada, te renderiza a la vista 'wait'
  - Si la compra está verificada, te redirecciona a la página principal
  
 - @app.route('/resume', methods=['GET']) 
  Esta ruta sirve para ver el resumen de la compra
   - Si la compra aun no se realizó, te renderiza al resumen
   - Si la compra se realiza, te redirecciona a la página principal
  

### Hosts

Local host 5000

### Manejo de Errores HTTP

- Para la sección del login del usuario:
  El servidor responde con código 400 si el usuario no existe o la contraseña es incorrecta, y 200 si es que todo ha ido bien.
  
- Para la sección de recuperar constraseña:
  El servidor responde con código 400 si al momento de verificar las credenciales del usuario estas no coinciden, o con código 200 si pasa lo contrario.
  
- Para la sección de crear usuario:
  El servidor responde con código 400 (BAD_REQUEST) si se trata de ingresar un correo ya registrado, o con código, o con código 200 si el registro es exitoso.
  
- Para la sección de busqueda:
  El servidor siempre responde con código 200, ya que el que encuentre resultados o no, no indica que la petición de busqueda no se haya realizado correctamente.
  
- Para la sección de compra:
  El servidor siempre responde con código 200, ya que lo único que se hace es una inserción de datos dentro de la base de datos con datos verificados en pasos anteriores.
  
- Para la sección de editar datos:
  El servidor siempre responde con código 200, ya que el único dato relevante para definir si hay un error o no al insertar datos en la base de datos es el correo, el cual ya esta restringido para edición desde el principio.
  
- Para la sección de compras realizadas por el usuario:
  El servidor siempre responde con código 200, ya que la petición de busqueda siempre se hace con los datos obtenido anteriormente, y lo único que varia es el contenido dentro del JSON que se devuelve.

### Ejecución del Sistema

Para ejecutar el sistema se tiene que correr server.py
