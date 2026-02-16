import { useState } from "react";
import useAIStore from "../store/ai.store";

export default function AIChat() {
  const { messages, sendMessage, isLoading } = useAIStore();
  const [input, setInput] = useState("");

  const send = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b flex items-center gap-3">
        <img src="/ai.png" className="size-10 rounded-full" />
        <div>
          <div className="font-medium">AI Assistant</div>
          <div className="text-xs text-zinc-400">Online</div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={m.role === "user" ? "text-right" : "text-left"}
          >
            <span className="bg-base-200 px-3 py-2 rounded inline-block">
              {m.text}
            </span>
          </div>
        ))}
        {isLoading && <div className="text-sm text-zinc-400">AI typing...</div>}
      </div>

      <div className="p-3 border-t flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask AI..."
          className="flex-1 border px-3 py-2 rounded"
        />
        <button onClick={send} className="bg-blue-500 text-white px-4 rounded">
          Send
        </button>
      </div>
    </div>
  );
}
