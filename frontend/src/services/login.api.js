import axios from "axios";
const BASE_URL = "http://localhost:5002/";

export const verifier_login = async () => {
  try {
    const { data } = await axios.get(BASE_URL);
    console.log(data);
  } catch (error) {
    window.location.href = "/login";
  }
};

export const login = async (user) => {
  try {
    const { data } = await axios.post(BASE_URL + "login", user);
    if (data.success) {
      window.location.href = "/";
    }
  } catch (error) {
    const message_error = document.getElementById("message_error");
    message_error.style.display = "block";
    message_error.innerHTML = error.response.data.message;
  }
};

export const logout = async () => {
  try {
    const { data } = await axios.get(BASE_URL + "logout");
    if (data.success) {
      window.location.href = "/login";
    }
  } catch (error) {
    console.log(error);
  }
};
