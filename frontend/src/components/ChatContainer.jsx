import { useChatStore } from "../store/useChatStore";
import useAIStore from "../store/ai.store";
import { useEffect, useRef } from "react";

import ChatHeader from "./ChatHeader";
import MessageInput from "./MessageInput";
import MessageSkeleton from "./skeletons/MessageSkeleton";

import { useAuthStore } from "../store/useAuthStore";
import { formatMessageTime } from "../lib/utils";

const ChatContainer = () => {
  const {
    messages,
    getMessages,
    isMessagesLoading,
    selectedUser,
    subscribeToMessages,
    unsubscribeFromMessages,
  } = useChatStore();

  const { messages: aiMessages } = useAIStore();
  const { authUser } = useAuthStore();
  const messageEndRef = useRef(null);

  const isAI = selectedUser?._id === "ai_assistant";

  // load normal chat only if not AI
  useEffect(() => {
    if (!selectedUser?._id || isAI) return;

    getMessages(selectedUser._id);
    subscribeToMessages();

    return () => unsubscribeFromMessages();
  }, [
    selectedUser?._id,
    isAI,
    getMessages,
    subscribeToMessages,
    unsubscribeFromMessages,
  ]);

  // scroll for both
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, aiMessages]);

  // loading
  if (!isAI && isMessagesLoading) {
    return (
      <div className="flex-1 flex flex-col overflow-auto">
        <ChatHeader />
        <MessageSkeleton />
        <MessageInput />
      </div>
    );
  }

  // choose data source
  const chatMessages = isAI
    ? aiMessages.map((m, i) => ({
        _id: i,
        text: m.text,
        senderId: m.role === "user" ? authUser._id : "ai",
        createdAt: new Date(),
      }))
    : messages;

  return (
    <div className="flex-1 flex flex-col overflow-auto">
      <ChatHeader />

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatMessages.map((message, idx) => {
          const isMe = message.senderId === authUser._id;
          const isLast = idx === chatMessages.length - 1;

          return (
            <div
              key={message._id}
              className={`chat ${isMe ? "chat-end" : "chat-start"}`}
            >
              <div className="chat-image avatar">
                <div className="size-10 rounded-full border">
                  <img
                    src={
                      isMe
                        ? authUser.profilePic || "/avatar.png"
                        : isAI
                          ? "/ai.png"
                          : selectedUser.profilePic || "/avatar.png"
                    }
                    alt="profile"
                  />
                </div>
              </div>

              <div className="chat-header mb-1">
                {!isAI && (
                  <time className="text-xs opacity-50 ml-1">
                    {formatMessageTime(message.createdAt)}
                  </time>
                )}
              </div>

              <div
                className="chat-bubble flex flex-col max-w-[70%]
                break-words break-all whitespace-pre-wrap"
                ref={isLast ? messageEndRef : null}
              >
                {message.text && <p>{message.text}</p>}
              </div>
            </div>
          );
        })}
      </div>

      {/* normal input OR AI input */}
      {isAI ? <MessageInput isAI /> : <MessageInput />}
    </div>
  );
};

export default ChatContainer;
