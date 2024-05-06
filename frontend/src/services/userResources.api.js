import axios from "axios";
import { BASE_URL } from "./url.js";

const COMPRA_URL = `${BASE_URL}compra`;

export const getCompras = async () => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };

  try {
    const { data } = await axios.get(COMPRA_URL, config);
    return data;
  } catch (error) {
    console.log(error);
  }

  return {};
};
