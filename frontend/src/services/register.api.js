import axios from "axios";
const BASE_URL = "http://localhost:5002/usuarios";

export const register = async (user) => {
  try {
    const { data } = await axios.post(BASE_URL, user);
    if (data.success) {
      window.location.href = "/";
    }
  } catch (error) {
    console.log(error.response.data);
    const message_error = document.getElementById("message_error");
    message_error.style.display = "block";
    message_error.innerHTML = error.response.data.message;
  }
};
