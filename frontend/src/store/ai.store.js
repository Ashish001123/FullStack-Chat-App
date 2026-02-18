import { create } from "zustand";
import { axiosInstance } from "../lib/axios";
import { useAuthStore } from "./useAuthStore";

const useAIStore = create((set, get) => ({
  messages: [],
  isLoading: false,

  // sendMessage: async (text) => {
  //   const authUser = useAuthStore.getState().authUser;

  //   if (!authUser) return;

  //   const userMsg = { role: "user", text };

  //   set((s) => ({
  //     messages: [...s.messages, userMsg],
  //     isLoading: true,
  //   }));

  //   const response = await axiosInstance.post("/ai", {
  //     messages: [...get().messages, { role: "user", content: text }],
  //   });
  //   const aiMsg = { role: "ai", text: response.data.reply };

  //   set((s) => ({
  //     messages: [...s.messages, aiMsg],
  //     isLoading: false,
  //   }));
  // },
  sendMessage: async (text) => {
  const authUser = useAuthStore.getState().authUser;
  if (!authUser) return;

  const userMsg = { role: "user", text };

  set((s) => ({
    messages: [...s.messages, userMsg],
    isLoading: true,
  }));

  const response = await axiosInstance.post("/ai", {
    text,
    userId: authUser._id,
  });

  const aiMsg = { role: "ai", text: response.data.reply };

  set((s) => ({
    messages: [...s.messages, aiMsg],
    isLoading: false,
  }));
}
}));

export default useAIStore;
