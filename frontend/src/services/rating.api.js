import Swal from "sweetalert2";
import axios from "axios";
import { BASE_URL } from "./url.js";

let URL_port = `${BASE_URL}:8022/`;

export const confirmRating = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de puntaje",
      text: "¿Estás seguro de que quieres publicar un puntaje para este juego?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#01d28e",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí",
      cancelButtonText: "Ya no",
      background: "#24283b",
      color: "white",
    }).then((result) => {
      resolve(result);
    });
  });
};

export const confirmUpdateRating = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de puntaje",
      text: "¿Estás seguro de actualizar tu puntaje de este juego?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#01d28e",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí",
      cancelButtonText: "Ya no",
      background: "#24283b",
      color: "white",
    }).then((result) => {
      resolve(result);
    });
  });
};

const confirmationRating = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de puntaje",
      text: "Tu puntaje de este juego se ha puclado exitosamente",
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

export const confirmateDeletionRating = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmar eliminación de puntaje",
      text: "¿Estás seguro de que quieres eliminar este puntaje? Esta acción no se puede deshacer.",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#01d28e",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Ya no",
      background: "#24283b",
      color: "white",
    }).then((result) => {
      resolve(result);
    });
  });
};

const confirmationUpdateRating = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de cambio de puntaje",
      text: "Tu puntaje de este juego se ha actualizado con exito",
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

export const createRating = async (ratingData) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.post(URL_port + "rating", ratingData, config);
    if (data.success) {
      const result = await confirmationRating();
      if (result.isConfirmed) {
        window.location.href = "/ratings";
      } else {
        window.location.href = "/ratings";
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

export const getRatings = async () => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "rating", config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const getRatingGame = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "rating/avg/" + id, config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const deleteRating = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.delete(URL_port + "rating/" + id, config);
    if (data.success) {
      Swal.fire({
        title: "Listo",
        text: "El puntaje se ha eliminado con éxito",
        icon: "success",
        showCancelButton: false,
        confirmButtonColor: "#01d28e",
        confirmButtonText: "Okey",
        background: "#24283b",
        color: "white",
      });
    } else {
      Swal.fire({
        title: "Error",
        text: data.message,
        icon: "error",
        showCancelButton: false,
        confirmButtonColor: "#d33",
        confirmButtonText: "Okey",
        background: "#24283b",
        color: "white",
      });
    }
  } catch (error) {
    console.log(error.response);
  }
};

export const getRatingById = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "rating/" + id, config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const updateRating = async (id, ratingData) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.patch(
      URL_port + "rating/" + id,
      ratingData,
      config
    );
    if (data.success) {
      const result = await confirmationUpdateRating();
      if (result.isConfirmed) {
        window.location.href = "/ratings";
      } else {
        window.location.href = "/ratings";
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
