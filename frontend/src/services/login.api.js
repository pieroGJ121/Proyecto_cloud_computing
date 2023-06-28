import axios from "axios";

const API_URL = "http://localhost:5002/";

export const verifier_login = async () => {
  const {
    data: { success },
  } = await axios.get(API_URL);
  if (!success) {
    window.location.href = "/login";
  }
};
