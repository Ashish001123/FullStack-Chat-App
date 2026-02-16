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

   const aiRes = await axios.post(
  process.env.AI_URL,
  { message }
);

    res.json({ reply: aiRes.data.reply });
  } catch (err) {
    console.error("AI error:", err.response?.data || err.message);
    res.status(500).json({ error: "AI failed" });
  }
});

export default router;