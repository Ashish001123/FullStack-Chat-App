import { create } from "zustand";
import { axiosInstance } from "../lib/axios.js";

export const useAIStore = create((set) => ({
  messages: [],
  loading: false,
  error: null,

  sendMessage: async (text) => {
    set((state) => ({
      messages: [...state.messages, { role: "user", content: text }],
      loading: true,
      error: null,
    }));
    try {
      const res = await axiosInstance.post("/ai", {
        text,
      });

      set((state) => ({
        messages: [
          ...state.messages,
          {
            role: "assistant",
            content: res.data.reply || res.data.response || "No response",
          },
        ],
        loading: false,
        error: null,
      }));
    } catch (error) {
      set({
        loading: false,
        error: error.message,
      });
    }
  },
}));
