import { create } from "zustand";
import { axiosInstance } from "../lib/axios";
import { useAuthStore } from "./useAuthStore";

const useAIStore = create((set) => ({
  messages: [],
  isLoading: false,

  sendMessage: async (text) => {
    const authUser = useAuthStore.getState().authUser;

    if (!authUser) return;

    const userMsg = { role: "user", text };

    set((s) => ({
      messages: [...s.messages, userMsg],
      isLoading: true,
    }));

    const res = await axiosInstance.post("/ai", {
      message: text,
      userId: authUser._id, 
    });

    const aiMsg = { role: "ai", text: res.data.reply };

    set((s) => ({
      messages: [...s.messages, aiMsg],
      isLoading: false,
    }));
  },
}));

export default useAIStore;
