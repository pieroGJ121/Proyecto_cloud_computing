import axios from "axios";

const BASE_URL = "http://localhost:5002/search/";

export const getGenres = async () => {
  try {
    const { data } = await axios.get(BASE_URL + "genres");
    return data;
  } catch (error) {
    console.error(error);
  }
  return [];
};

export const getPlatforms = async () => {
  try {
    const { data } = await axios.get(BASE_URL + "platforms");
    return data;
  } catch (error) {
    console.error(error);
  }
  return [];
};

export const getGames = async () => {
  const url = new URL(window.location.href);
  try {
    const { data } = await axios.get(BASE_URL + "search_query" + url.search);
    console.log(data);
  } catch (error) {
    console.error(error.response);
  }

  return [];
};
