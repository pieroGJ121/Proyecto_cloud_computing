import axios from "axios";
const BASE_URL = "http://localhost:5002/create";

export const register = async (user) => {
  try {
    const { data } = await axios.post(BASE_URL, user);
    if (data.success) {
      sessionStorage.setItem("token", data.token);
      sessionStorage.setItem("user_id", data.usuario_id);
      window.location.href = "/";
    } else {
      return data.errors;
    }
  } catch (error) {
    const message_error = document.getElementById("message_error");
    message_error.style.display = "block";
    message_error.innerHTML =
      "Ha ocurrido un error. Vuelve a intentarlo mas tarde 😪";
  }
  return [];
};
