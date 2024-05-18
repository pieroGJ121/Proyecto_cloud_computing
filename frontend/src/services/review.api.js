import Swal from "sweetalert2";
import axios from "axios";
import { BASE_URL } from "./url.js";

let URL_port = `${BASE_URL}:8021/`;

export const confirmReview = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de review",
      text: "¿Estás seguro de que quieres publicar esta reseña?",
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

export const confirmUpdateReview = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de reseña",
      text: "¿Estás seguro de actualizar los datos de esta reseña?",
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

const confirmationReview = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de reseña",
      text: "Tu reseña de este juego se ha realizado con éxito",
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

export const confirmDeletionReview = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmar eliminación de reseña",
      text: "¿Estás seguro de que quieres eliminar esta reseña? Esta acción no se puede deshacer.",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#01d28e",
      confirmButtonText: "Si, eliminar",
      cancelButtonText: "Ya no",
      background: "#24283b",
      color: "white",
    }).then((result) => {
      resolve(result);
    });
  });
};

const confirmationUpdateReview = () => {
  return new Promise((resolve) => {
    Swal.fire({
      title: "Confirmación de cambio de reseña",
      text: "Tu reseña de este juego se ha actualizado con exito",
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

export const createReview = async (reviewData) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.post(URL_port + "review", reviewData, config);
    if (data.success) {
      const result = await confirmationReview();
      if (result.isConfirmed) {
        window.location.href = "/reviews";
      } else {
        window.location.href = "/reviews";
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

export const getReviews = async () => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "review", config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const getReviewsGame = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "review/game/" + id, config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const deleteReview = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.delete(URL_port + "review/" + id, config);
    if (data.success) {
      Swal.fire({
        title: "Listo",
        text: "La reseña se ha eliminado con éxito",
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

export const getReviewById = async (id) => {
  const headers = {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": sessionStorage.getItem("token"),
    "user-id": sessionStorage.getItem("user_id"),
  };
  const config = {
    headers: headers,
  };
  try {
    const { data } = await axios.get(URL_port + "review/" + id, config);
    return data;
  } catch (error) {
    console.log(error.response);
  }
  return {};
};

export const updateReview = async (id, reviewData) => {
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
      URL_port + "review/" + id,
      reviewData,
      config
    );
    if (data.success) {
      const result = await confirmationUpdateReview();
      if (result.isConfirmed) {
        window.location.href = "/reviews";
      } else {
        window.location.href = "/reviews";
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
