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

export const login = async (email, password) => {
  const formData = new FormData();
  formData.append("email", email);
  formData.append("password", password);

  try {
    const { data } = await axios.post(BASE_URL + "login", formData);
    if (data.success) {
      window.location.href = "/";
    }
  } catch (error) {
    if (!error.response.data.success) {
      const message_error = document.getElementById("message_error");
      message_error.style.display = "block";
      message_error.innerHTML = error.response.data.message;
    } else {
      const message_error = document.getElementById("message_error");
      message_error.style.display = "block";
      message_error.innerHTML =
        "Lo sentimos, estamos experimentando problemas. Inténtelo de nuevo más tarde 😪";
    }
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
