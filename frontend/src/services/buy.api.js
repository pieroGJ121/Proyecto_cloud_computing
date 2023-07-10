import axios from "axios";
const BASE_URL = "http://localhost:5002/compra";

export const comprarJuego = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  const data_post = {
    id: id,
  };
  try {
    console.log(config);
    const { data } = await axios.post(BASE_URL, data_post, config);
    console.log(data);
  } catch (error) {
    console.log(error.response);
  }
};
