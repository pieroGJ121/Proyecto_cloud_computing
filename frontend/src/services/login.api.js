import axios from "axios";
import { BASE_URL } from "./url.js";

let URL_port = `${BASE_URL}:8023/`;

export const verifier_login = async () => {
  if (sessionStorage.getItem("token") === null) {
    window.location.href = "/login";
  }
};

export const login = async (user) => {
  try {
    const { data } = await axios.post(URL_port + "login", user);
    if (data.success) {
      sessionStorage.setItem("token", data.token);
      sessionStorage.setItem("user_id", data.usuario_id);
      window.location.href = "/";
    } else {
      const message_error = document.getElementById("message_error");
      message_error.style.display = "block";
      message_error.innerHTML = data.errors;
    }
  } catch (error) {
    const message_error = document.getElementById("message_error");
    message_error.style.display = "block";
    message_error.innerHTML =
      "Ha ocurrido un error. Vuelve a intentarlo mas tarde 😪";
  }
};

export const logout = async () => {
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("user_id");
  window.location.href = "/login";
};
