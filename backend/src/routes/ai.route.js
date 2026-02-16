// import express from "express";
// const router = express.Router();

// router.post("/", async (req, res) => {
//   try {
//     const { message } = req.body;

//     const response = await fetch(process.env.AI_URL, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ message }),
//     });

//     const data = await response.json();

//     res.json({ reply: data.reply });

//   } catch (err) {
//     console.error("AI ERROR:", err);
//     res.status(500).json({ error: "AI failed" });
//   }
// });

// export default router;



import express from "express";
import axios from "axios";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { message } = req.body;

    const aiRes = await axios.post(
      process.env.AI_URL,
      { message },
      { timeout: 20000 } // allow Render cold start
    );

    res.json({ reply: aiRes.data.reply });

  } catch (err) {
    console.error("AI ERROR:", err.response?.data || err.message);
    res.status(500).json({ error: "AI failed" });
  }
});

export default router;