import express from "express";
import axios from "axios";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { message } = req.body;

    const aiRes = await axios.post(
      "http://localhost:8000/chat",
      { message }
    );

    res.json({ reply: aiRes.data.reply });
  } catch (err) {
    res.status(500).json({ error: "AI failed" });
  }
});

export default router;