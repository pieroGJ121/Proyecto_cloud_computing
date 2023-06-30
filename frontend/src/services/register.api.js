import axios from "axios";
const BASE_URL = "http://localhost:5002/";

export const register = async (name, lastname, bio, email, password) => {
  const formData = new FormData();
  formData.append("name", name);
  formData.append("lastname", lastname);
  formData.append("bio", bio);
  formData.append("email", email);
  formData.append("password", password);

  try {
    const { data } = await axios.post(BASE_URL + "new_user", formData);
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
