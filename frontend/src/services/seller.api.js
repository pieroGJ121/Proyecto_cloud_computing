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

const confirmationOffer = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de venta",
      text: "Tu oferta de este juego se ha realizado con éxito",
      icon: "success",
      showCancelButton: false,
      confirmButtonColor: "#01d28e",
      confirmButtonText: "Okey",
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
    if (data.success) {
      const result = await confirmationOffer();
      if (result.isConfirmed) {
        window.location.href = "/";
      } else {
        window.location.href = "/";
      }
    } else {
      Swal.fire({
        title: "Error",
        text: data.message,
        icon: "error",
        showCancelButton: false,
        confirmButtonColor: "#d33",
        confirmButtonText: "Okey :(",
        background: "#24283b",
        color: "white",
      });
    }
  } catch (error) {
    console.log(error.response);
  }
};

export const getSales = async () => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(BASE_URL + "oferta", config);
    console.log(data);
  } catch (error) {
    console.log(error.response);
  }
};
