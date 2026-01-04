import { create } from "zustand";
import toast from "react-hot-toast";
import { axiosInstance } from "../lib/axios";
import { useAuthStore } from "./useAuthStore";

export const useChatStore = create((set, get) => ({
  messages: [],
  users: [],
  selectedUser: null,
  isUsersLoading: false,
  isMessagesLoading: false,

  getUsers: async () => {
    set({ isUsersLoading: true });
    try {
      const res = await axiosInstance.get("/messages/users");
      const usersWithUnread = res.data.map((u) => ({
        ...u,
        unreadCount: u.unreadCount || 0,
      }));

      set({ users: usersWithUnread });
    } catch (error) {
      toast.error(error.response?.data?.message || "Failed to load users");
    } finally {
      set({ isUsersLoading: false });
    }
  },

  getMessages: async (userId) => {
    set({ isMessagesLoading: true });
    try {
      const res = await axiosInstance.get(`/messages/${userId}`);
      set({ messages: res.data });
    } catch (error) {
      toast.error(error.response?.data?.message || "Failed to load messages");
    } finally {
      set({ isMessagesLoading: false });
    }
  },

  sendMessage: async (messageData) => {
    const { selectedUser, messages } = get();
    try {
      const res = await axiosInstance.post(
        `/messages/send/${selectedUser._id}`,
        messageData
      );

      set({ messages: [...messages, res.data] });
    } catch (error) {
      toast.error(error.response?.data?.message || "Failed to send message");
    }
  },

  subscribeToMessages: () => {
    const socket = useAuthStore.getState().socket;
    if (!socket) return;

    socket.on("newMessage", (newMessage) => {
      const { selectedUser, messages } = get();

      // If chat is open, append message
      if (selectedUser && newMessage.senderId === selectedUser._id) {
        set({ messages: [...messages, newMessage] });
        return;
      }

      // Otherwise update sidebar (unread + move to top)
      get().receiveMessage(newMessage);
    });
  },

  unsubscribeFromMessages: () => {
    const socket = useAuthStore.getState().socket;
    socket?.off("newMessage");
  },

  receiveMessage: (message) =>
    set((state) => {
      const senderId = message.senderId;

      const updatedUsers = state.users.map((u) =>
        u._id === senderId
          ? { ...u, unreadCount: (u.unreadCount || 0) + 1 }
          : u
      );

      const sender = updatedUsers.find((u) => u._id === senderId);
      const rest = updatedUsers.filter((u) => u._id !== senderId);

      return {
        users: sender ? [sender, ...rest] : updatedUsers,
      };
    }),

  clearUnread: (userId) =>
    set((state) => ({
      users: state.users.map((u) =>
        u._id === userId ? { ...u, unreadCount: 0 } : u
      ),
    })),
  
  clearChat: (userId) =>
  set((state) => ({
    messages: [],
    users: state.users.map((u) =>
      u._id === userId ? { ...u, unreadCount: 0 } : u
    ),
  })),


  setSelectedUser: (selectedUser) => set({ selectedUser }),
}));
