import axios from "axios";

const BASE_URL = "http://localhost:5002/search/";
const VIDEOGAME_URL = "http://localhost:5002/videogame/";

export const getGenres = async () => {
  try {
    const { data } = await axios.get(BASE_URL + "genres");
    return data;
  } catch (error) {
    console.error(error.response.data);
  }
  return [];
};

export const getPlatforms = async () => {
  try {
    const { data } = await axios.get(BASE_URL + "platforms");
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
      BASE_URL + "search_query" + url.search
    );

    let resultsApi = games.games;
    let results = [];

    resultsApi.forEach((game) => {
      results.push(getGameData(game.id));
    });

    results = await Promise.all(results);

    results = results.filter((objeto) => Object.keys(objeto).length !== 0);

    return results;
  } catch (error) {
    console.error("Error al buscar algunos juegos...");
  }

  return [];
};

export const getGameData = async (id) => {
  try {
    const { data } = await axios.get(VIDEOGAME_URL + id);
    return data;
  } catch (error) {
    console.error("Error al buscar datos del juego", id);
  }
  return {};
};
