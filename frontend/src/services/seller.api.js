import Swal from "sweetalert2";
import axios from "axios";

const BASE_URL = "http://localhost:5002/";

export const confirmarVenta = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de venta",
      text: "¿Estás seguro de que quieres vender este juego?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#01d28e",
      cancelButtonColor: "#d33",
      confirmButtonText: "Obvio",
      cancelButtonText: "Ya no",
      background: "#24283b",
      color: "white",
    }).then((result) => {
      resolve(result);
    });
  });
};

export const createSale = async (sellData) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.post(BASE_URL + "oferta", sellData, config);
    console.log(data);
  } catch (error) {
    console.log(error.response);
  }
};
