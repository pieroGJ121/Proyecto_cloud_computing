<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/Fabrizzio20k/Proyecto_DBP">
  </a>
  <h1>👾 GPT VIDEOGAMES 👾</h1>
  
  <p>
  Este proyecto ha sido desarrollado por estudiantes del curso de Cloud Computing 
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
        <li><a href="#objetivo">Objetivo</a></li>
        <li><a href="#librerías-frameworks-y-plugins">Librerías, Frameworks y Plugins</a></li>
        <li><a href="#script">Script</a></li>
        <li><a href="#apis">API</a></li>
        <li><a href="#hosts">Hosts</a></li>
        <li><a href="#manejo-de-errores-http">Manejo de Errores HTTP</a></li>
        <li><a href="#ejecución-del-sistema">Ejecución del Sistema</a></li>
        <li><a href="#recursos-extra">Recursos extra</a></li>
        <li><a href="#equipo">Equipo</a></li>
      </ul>
    </a></li>
  </ol>
</details>

---

## Integrantes

- Piero Jesus Guerrero Jimenez
- Cesar Stefano Flores Uriarte

## Acerca del proyecto

### Descripción

Este proyecto consiste en el desarrollo de un sitio web llamadp GPT videogames, la
cual nos permite publicar reseñas sobre video juegos y además calificarlas con una puntuación

### Objetivo

Esta página tiene como misión llegar a ser de total comodidad para el cliente y un lugar
donde puedas consultar opiniones acerca de videojuegos. De esta manera podrás visualizar y
elegir un videojuego a tu propio criterio.


### Librerías, Frameworks y Plugins

Front-end:

- Vue.js es un framework de JavaScript de código abierto para construir 
interfaces de usuario. Es conocido por su simplicidad y rendimiento, permitiendo 
una integración fácil y un desarrollo basado en componentes. 
- Bootstrap: Bootstrap es un framework de desarrollo web gratuito y de código abierto. Está diseñado para facilitar el proceso de desarrollo de los sitios web responsivos y orientados a los dispositivos móviles, proporcionando una colección de sintaxis para diseños de plantillas.
- Slidy: Libreria de JS para mostrar un slide responsivo de manera fácil.
- SweetAlert2: Libreria de JS para mostrar alertas de forma más atractiva y con poco código.
- Axios: Libreria de JS para hacer diferentes peticiones al backend.

Back-end:

- Flask: Flask es un framework ligero de desarrollo web en Python que permite crear aplicaciones web rápidas y eficientes. Proporciona herramientas y bibliotecas para manejar solicitudes HTTP, enrutar URL, generar respuestas dinámicas y gestionar bases de datos. Flask es altamente personalizable y fácil de aprender, lo que lo convierte en una elección popular para desarrolladores de backend. Se usa en este proyecto para manejar las solicitudes a la base de datos y algunas operaciones de verificación.

- SQLAlchemy: SQLAlchemy es una biblioteca de mapeo objeto-relacional en Python que facilita la interacción con bases de datos relacionales. Proporciona una capa de abstracción que permite interactuar con la base de datos utilizando objetos y consultas en lugar de escribir consultas SQL directamente. SQLAlchemy simplifica el manejo de la persistencia de datos y la creación de consultas complejas.
- SMTPLIB: La biblioteca smtplib de Python se utiliza para enviar correos electrónicos a través de un servidor SMTP. Primero, se establece una conexión con el servidor utilizando smtplib.SMTP, luego se autentica con credenciales y se envía el correo utilizando sendmail. Todo esto se usa para enviar correos al usuario al final de la compra.

Base de Datos:

- Flask_migrate
- SQLAlchemy

### Script

Para cargar el backend se ejecuta:

```sh
./ejecutar.sh
```

- Se debe estar dentro de la siguiente ruta: backend/api_profiles.
- Después, se usa ejecuta el código de los sql scripts encontrados dentro de la carpete /sql. Estos añaden la exensión uuid-ossp en la base de datos.
- Finalmente, se inicia el servidor.
- Debe existir una base de datos con el nombre de "Proyecto_cloud_computing".

Para cargar el frontend se ejecuta:

```sh
npm install
npm run serve
```

- Se debe estar dentro de la carpeta llamada frontend, en el mismo nivel que la carpeta src.

### Testing

Para realizar el testing del backend se ejecuta:

```sh
python -m unittest Test.py
```

- Se debe estar dentro de la carpeta llamada backend, en el mismo nivel que la carpeta app.

### APIS
Api Games:

La API que se está utilizando se llama IGDB.com, el cual sirve para obtener información sobre videojuegos individuales y poder realizar búsquedas de videojuegos.

Api Profiles:

Profiles representa a los usuarios de la aplicación. Cada usuario tiene varios atributos clave que almacenan información personal.

Diagrama:

![Diseño Básico de la Página](https://raw.githubusercontent.com/pieroGJ121/Proyecto_cloud_computing/main/extra/Usuario.png)

Api Ratings:

Rating representa las valoraciones que los usuarios pueden hacer sobre los juegos.

Diagrama:

![Diseño Básico de la Página](https://raw.githubusercontent.com/pieroGJ121/Proyecto_cloud_computing/main/extra/Review.png)

Api Reviews:

Review representa las reseñas que los usuarios pueden hacer sobre los juegos en la aplicación.

Diagrama:

![Diseño Básico de la Página](https://raw.githubusercontent.com/pieroGJ121/Proyecto_cloud_computing/main/extra/Rating.png)
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
- Para la sección de reseñas:
  El servidor siempre responde con código 200, ya que lo único que se hace es una inserción de datos dentro de la base de datos con datos verificados en pasos anteriores.
- Para la sección de editar datos:
  El servidor siempre responde con código 200, ya que el único dato relevante para definir si hay un error o no al insertar datos en la base de datos es el correo, el cual ya esta restringido para edición desde el principio.
- Para la sección de reseñas realizadas por el usuario:
  El servidor siempre responde con código 200, ya que la petición de busqueda siempre se hace con los datos obtenido anteriormente, y lo único que varia es el contenido dentro del JSON que se devuelve.

### Ejecución del Sistema

Para ejecutar el sistema se tiene que correr server.py

### Recursos extra

[Modelo entidad-relación de la base de datos implementada](extra/diagrama_entidad_solucion.png)
![diagrama de clases](https://raw.githubusercontent.com/pieroGJ121/Proyecto_cloud_computing/main/extra/diagrama_entidad_solucion.png)

[Automatización](extra/cont-start.sh)
```sh
#!/usr/bin/env sh
docker pull proyectoccgrupo7/frontend:latest
docker pull proyectoccgrupo7/api-games:latest
docker pull proyectoccgrupo7/api-reviews:latest
docker pull proyectoccgrupo7/api-ratings:latest
docker pull proyectoccgrupo7/api-profiles:latest

docker run -d -p 8030:3000 proyectoccgrupo7/frontend
docker run -d -p 8020:8020 proyectoccgrupo7/api-games
docker run -d -p 8021:8021 proyectoccgrupo7/api-reviews
docker run -d -p 8022:8022 proyectoccgrupo7/api-ratings
docker run -d -p 8023:8023 proyectoccgrupo7/api-profiles
```

[Docker-compose-deploy](extra/docker-compose-deploy.yml)
```yml
version: "3.3"

services:
  api-games:
    image: proyectoccgrupo7/api-games
    ports:
      - 8020:8020
  api-reviews:
    image: proyectoccgrupo7/api-reviews
    ports:
      - 8021:8020
  api-ratings:
    image: proyectoccgrupo7/api-ratings
    ports:
      - 8022:8020
  api-profiles:
    image: proyectoccgrupo7/api-profiles
    ports:
      - 8023:8020
  frontend:
    image: proyectoccgrupo7/frontend
    ports:
      - 8040:3000
```

### Equipo

|Piero Guerrero|Cesar Flores|
|---------------------------------------------------------- | --------------------------------------------------------- |
| ![](https://avatars.githubusercontent.com/u/104638037?v=4) | ![](https://avatars.githubusercontent.com/u/142551373?s=96&v=4) |
| [github.com/pieroGJ121](https://github.com/pieroGJ121).    | [github.com/stefano565-Utec](https://github.com/stefano565-Utec)      |
