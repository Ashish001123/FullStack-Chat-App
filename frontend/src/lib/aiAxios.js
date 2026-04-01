// import axios from "axios";

// export const axiosInstance = axios.create({
//     baseURL: "http://localhost:8000",
//     withCredentials: true,
//     headers: {
//         "Content-Type" : "application/json"
//     }
// })



import axios from "axios";

const AI_URL =
  import.meta.env.VITE_AI_URL ||
  "http://localhost:8000";

export const aiAxiosInstance = axios.create({
  baseURL: AI_URL,
});