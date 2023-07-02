import axios from "axios";
const BASE_URL = "http://localhost:5002/profile_data";

export const getUserData = async (user) => {
  try {
    const { data } = await axios.get(BASE_URL, user);
    if (data.success) {
      return data.user;
    }
  } catch (error) {
    console.log(error.response.data);
  }
  return {
    username: "",
    lastname: "",
    email: "",
    bio: "",
    password: "",
  };
};

export const updateUserData = async (user) => {
  const message_error = document.getElementById("message_error");
  try {
    const { data } = await axios.patch(BASE_URL, user);
    if (data.success) {
      message_error.style.display = "none";
      window.location.href = "/";
    }
  } catch (error) {
    message_error.style.display = "block";
    message_error.innerHTML = error.response.data.message;
    console.log(error);
  }
};

export const deleteUser = async (user) => {
  const message_error = document.getElementById("message_error");
  try {
    const { data } = await axios.delete(BASE_URL, user);
    if (data.success) {
      message_error.style.display = "none";
      window.location.href = "/";
    }
  } catch (error) {
    message_error.style.display = "block";
    message_error.innerHTML = error.response.data.message;
  }
};
