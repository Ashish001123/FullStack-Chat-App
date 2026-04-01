// import { create } from "zustand";
// import { axiosInstance } from "../lib/axios";
// import { useAuthStore } from "./useAuthStore";

// const useAIStore = create((set, get) => ({
//   messages: [],
//   isLoading: false,

//   sendMessage: async (text) => {
//   const authUser = useAuthStore.getState().authUser;
//   if (!authUser) return;

//   const userMsg = { role: "user", text };

//   set((s) => ({
//     messages: [...s.messages, userMsg],
//     isLoading: true,
//   }));

//   const response = await axiosInstance.post("/ai", {
//     text,
//     userId: authUser._id,
//   });

//   const aiMsg = { role: "ai", text: response.data.reply };

//   set((s) => ({
//     messages: [...s.messages, aiMsg],
//     isLoading: false,
//   }));
// }
// }));

// export default useAIStore;



import { create } from "zustand"
import { axiosInstance } from "../lib/aiAxios.js"


export const useAIStore = create((set) => ({
  messages: [],
  loading: false,
  error: null, 

  sendMessage: async (text) => {
    set((state) => ({
      messages: [...state.messages, { role: "user", content: text }],
        loading: true,
        error: null
    }))
    try {
      const res = await axiosInstance.post("/chat", {
        message : text
      });

    set((state) => ({
      messages: [...state.messages, { role: "assistant", content: res.data.result || res.data.response || "No response"}],
        loading: false,
        error: null
    }))
}
  catch (error) {
      set({
        loading: false,
        error: error.message
      })
    }
  }
}))