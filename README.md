<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/CS1103/proyecto-final-2023_0-proyecto-final-2023_0-grupo-5">
    <img src="extra/square_maze.jpg" alt="hex board" width="150" height="150">
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
        <li><a href="#api">API</a></li>
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

Este juego tiene como objetivo ofrecer posibilidades
infinitas a la hora de jugar, ya que ningun juego será igual que el anterior, además
de poder configurar algunos aspectos del juego antes de empezar para mejorar la
experiencia. No obstante, el juego también permite decidir la forma de jugar, ya sea
entre un jugador de manera local, u contra la misma computadora.

### Objetivos Principales

#### Misión

Esta página tiene como misión llegar a ser de total comodidad para el cliente y cumplirlo ofreciendo videojuegos de alta calidad.

#### Visión

La visión de esta página es 

### Librerías, Frameworks y Plugins

- Todas las que hemos visto en clase (mencionarlas)

### Script

- Backtracking algorithm to generate random mazes
- Deep-First Search to find the path in the maze
- Breadth-First Search to find the shortest path in the maze
- Using Raylib library to create games with C++

### API

fwefuqwegfgwuef

### Hosts

lskdfajsdfjsdf

### Manejo de Errores HTTP

- Log in del usuario

### Ejecución del Sistema

kASKAJFASKDF





## Instrucciones de uso

### Instrucciones

### Reglas de juego

El juego MAZERS genera un laberinto de tamaño (n x m), y a partir de aquí se puede hacer lo siguiete:

- Al comienzo de cada partida se genera un laberinto con recuadros llenos o vacios (paredes y espacios para moverse).
- Cada jugador cuenta con un indicador cuadrado de un color distinto al otro. (Siempre son 2 jugadores)
- Los movimientos se harán por turnos de manera consecutiva, donde es posible moverse en cualquier dirección siempre y cuando haya un recuadro de espacio disponible como mínimo.
- El movimiento se hace hasta encontrar una bifurcación (2 o más caminos disponibles). Siempre se avanza todas las casillas disponibles hasta que haya varios caminos, o no haya caminos disponibles y solo se pueda regresar al punto de control de donde se realizó el movimiento.
- La finalidad del juego es llegar a la meta (el centro de laberinto) antes que el otro jugador.
- Gana el jugador que llegue primero al centro del laberinto (objetivo).
