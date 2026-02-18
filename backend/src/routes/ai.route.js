import express from "express";
import axios from "axios";
import Message from "../models/message.model.js";
import User from "../models/user.model.js";
const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { text, userId } = req.body;
    const message = text;
    const history = await Message.find({
      $or: [
        { senderId: userId, receiverId: "ai_assistant" },
        { senderId: "ai_assistant", receiverId: userId },
      ],
    })
      .sort({ createdAt: -1 })
      .limit(20)
      .lean();
    const messages = history.reverse().map((m) => ({
      role: m.senderId === "ai_assistant" ? "assistant" : "user",
      content: m.text,
    }));
    messages.push({ role: "user", content: message });
    const aiRes = await axios.post(process.env.AI_URL, {
      messages,
    });

    const reply = aiRes.data.reply;
    await Message.create({
      senderId: userId,
      receiverId: "ai_assistant",
      text: message,
    });
    await Message.create({
      senderId: "ai_assistant",
      receiverId: userId,
      text: reply,
    });
    res.json({ reply });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "AI failed" });
  }
});

router.get("/user", async (req, res) => {
  try {
    const users = await User.find().select("-password");
    res.json(users);
  } catch (e) {
    console.error("AI users error", e);
    res.status(500).json({ error: "failed" });
  }
});

export default router;
