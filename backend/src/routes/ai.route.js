// import express from "express";
// import axios from "axios";

// const router = express.Router();

// const AI_URL = process.env.AI_URL;

// router.post("/", async (req, res) => {
//   try {
//     const { message } = req.body;

//     const aiRes = await axios.post(
//       `${AI_URL}`,
//       { message }
//     );

//     res.json({ reply: aiRes.data.reply });
//   } catch (err) {
//     console.error("AI error:", err.message);
//     res.status(500).json({ error: "AI failed" });
//   }
// });

// export default router;


import express from "express";
import axios from "axios";

const router = express.Router();

const AI_URL = process.env.AI_URL;

router.post("/", async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: "Message required" });
    }

    // 🔥 call AI with timeout (Render cold start safe)
    const aiRes = await axios.post(
      AI_URL,
      { message },
      {
        timeout: 20000, // 20s for Render wake-up
      }
    );

    if (!aiRes.data?.reply) {
      throw new Error("Invalid AI response");
    }

    res.json({ reply: aiRes.data.reply });

  } catch (err) {
    console.error("AI ERROR:", err.message);

    res.status(500).json({
      error: "AI failed",
      details: err.message,
    });
  }
});

export default router;