import axios from "axios";
const BASE_URL = "http://localhost:5002/";

export const validateData = async (user) => {
  const message_error = document.getElementById("message_error");
  const password_changer = document.getElementById("password_changer");
  const submit1 = document.getElementById("submit1");
  const email = document.getElementById("email");
  const name = document.getElementById("name");
  const text_email = document.getElementById("text_email");
  const text_name = document.getElementById("text_name");
  const text_change = document.getElementById("text_change");

  try {
    const { data } = await axios.post(BASE_URL + "data_recovery", user);
    if (data.success) {
      message_error.style.display = "none";
      password_changer.style.display = "block";
      submit1.style.display = "none";
      text_change.style.display = "block";
      email.disabled = true;
      name.disabled = true;
      text_email.innerHTML = "";
      text_name.innerHTML = "";
    }
  } catch (error) {
    message_error.style.display = "block";
    password_changer.style.display = "none";
    message_error.innerHTML = error.response.data.message;
    text_change.style.display = "none";
  }
};

export const resetPassword = async (user) => {
  const message_error = document.getElementById("message_error2");
  try {
    const { data } = await axios.post(BASE_URL + "password_recovery", user);
    if (data.success) {
      message_error.style.display = "none";
      window.location.href = "/login";
    }
  } catch (error) {
    message_error.style.display = "block";
    message_error.innerHTML = error.response.data.message;
  }
};
