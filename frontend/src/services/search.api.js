import axios from "axios";
import { BASE_URL } from "./url.js";

let URL_port = `${BASE_URL}:8020/`;

const SEARCH_URL = `${URL_port}search/`;
const VIDEOGAME_URL = `${URL_port}videogame/`;

export const getGenres = async () => {
  try {
    const { data } = await axios.get(SEARCH_URL + "genres", {
      headers: {
        "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
      },
    });
    return data;
  } catch (error) {
    console.error(error.response.data);
  }
  return [];
};

export const getPlatforms = async () => {
  try {
    const { data } = await axios.get(SEARCH_URL + "platforms", {
      headers: {
        "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
      },
    });
    return data;
  } catch (error) {
    console.error(error.response.data);
  }
  return [];
};

export const getGames = async () => {
  const url = new URL(window.location.href);
  try {
    const { data: games = {} } = await axios.get(
      SEARCH_URL + "search_query" + url.search,
      {
        headers: {
          "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
        },
      }
    );

    let results = games.games;
    console.log(results);

    return results;
  } catch (error) {
    console.error("Error al buscar algunos juegos...");
  }

  return [];
};

export const getGameData = async (id) => {
  try {
    const { data } = await axios.get(VIDEOGAME_URL + id, {
      headers: {
        "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
      },
    });
    return data;
  } catch (error) {
    console.error("Error al buscar datos del juego", id);
  }
  return {};
};

export const formatearFecha = (fechaString) => {
  const fecha = new Date(fechaString);

  const opciones = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    timeZone: "UTC",
  };

  const formatoFecha = fecha.toLocaleString("es-ES", opciones);
  return formatoFecha;
};
