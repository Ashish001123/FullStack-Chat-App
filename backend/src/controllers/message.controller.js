import User from "../models/user.model.js";
import Message from "../models/message.model.js";

import cloudinary from "../lib/cloudinary.js";
import { getReceiverSocketId, io } from "../lib/socket.js";

export const getUsersForSidebar = async (req, res) => {
  try {
    const loggedInUserId = req.user._id;

    const users = await User.find({
      _id: { $ne: loggedInUserId },
    }).select("-password");
    const unreadCounts = await Message.aggregate([
  {
    $match: {
      receiverId: loggedInUserId,
      isRead: false,
    },
  },
  {
    $group: {
      _id: "$senderId",
      count: { $sum: 1 },
    },
  },
]);
    const unreadMap = {};
    unreadCounts.forEach((u) => {
      unreadMap[u._id.toString()] = u.count;
    });

    const usersWithUnread = users.map((user) => ({
      ...user.toObject(),
      unreadCount: unreadMap[user._id.toString()] || 0,
    }));

    res.status(200).json(usersWithUnread);
  } catch (error) {
    console.error("Error in getUsersForSidebar:", error.message);
    res.status(500).json({ error: "Internal server error" });
  }
};



// export const getMessages = async (req, res) => {
//   try {
//     const { id: userToChatId } = req.params;
//     const myId = req.user._id;

//     const messages = await Message.find({
//       $or: [
//         { senderId: myId, receiverId: userToChatId },
//         { senderId: userToChatId, receiverId: myId },
//       ],
//       deletedFor: { $ne: myId }, 
//     }).sort({ createdAt: 1 });

//     res.status(200).json(messages);
//   } catch (error) {
//     console.log("Error in getMessages controller:", error.message);
//     res.status(500).json({ error: "Internal server error" });
//   }
// };


export const getMessages = async (req, res) => {
  try {
    const myId = req.user._id.toString();
    const userToChatId = req.params.id.toString();

    const messages = await Message.find({
      $and: [
        {
          $or: [
            { senderId: myId, receiverId: userToChatId },
            { senderId: userToChatId, receiverId: myId },
          ],
        },
        {
          $or: [
            { deletedFor: { $exists: false } },
            { deletedFor: { $nin: [req.user._id] } },
          ],
        },
      ],
    }).sort({ createdAt: 1 });

    res.status(200).json(messages);
  } catch (error) {
    console.log("Error in getMessages:", error.message);
    res.status(500).json({ error: "Internal server error" });
  }
};


// export const sendMessage = async (req, res) => {
//   try {
//     const { text, image } = req.body;
//     const { id: receiverId } = req.params;
//     const senderId = req.user._id;

//     if (receiverId === "ai_assistant") {
//       const aiReply = "Hello 👋 I'm your AI assistant";

//       const aiMessage = new Message({
//         senderId: "ai_assistant",
//         receiverId: senderId,
//         text: aiReply,
//         isRead: true,
//       });

//       await aiMessage.save();
//       return res.status(201).json(aiMessage);
//     }

//     let imageUrl = null;
//     if (image) {
//       const upload = await cloudinary.uploader.upload(image);
//       imageUrl = upload.secure_url;
//     }

//     const newMessage = new Message({
//       senderId,
//       receiverId,
//       text: text || "",
//       image: imageUrl,
//       isRead: false,
//     });

//     await newMessage.save();
//     const receiverSocketId = getReceiverSocketId(receiverId);
//     if (receiverSocketId) {
//       io.to(receiverSocketId).emit("newMessage", newMessage);
//     }
//     res.status(201).json(newMessage);
//   } catch (error) {
//     console.log("Error in sendMessage:", error.message);
//     res.status(500).json({ error: "Internal server error" });
//   }
// };



export const sendMessage = async (req, res) => {
  try {
    const { text, image } = req.body;
    const senderId = req.user._id.toString();
    const receiverId = req.params.id.toString();

    if (receiverId === "ai_assistant") {
      const aiMessage = new Message({
        senderId: "ai_assistant",
        receiverId: senderId,
        text: "Hello 👋 I'm your AI assistant",
        isRead: true,
      });

      await aiMessage.save();
      return res.status(201).json(aiMessage);
    }

    let imageUrl = null;
    if (image) {
      const upload = await cloudinary.uploader.upload(image);
      imageUrl = upload.secure_url;
    }

    const newMessage = new Message({
      senderId,
      receiverId,
      text: text || "",
      image: imageUrl,
      isRead: false,
    });

    await newMessage.save();

    const receiverSocketId = getReceiverSocketId(receiverId);
    if (receiverSocketId) {
      io.to(receiverSocketId).emit("newMessage", newMessage);
    }

    res.status(201).json(newMessage);
  } catch (error) {
    console.log("Error in sendMessage:", error.message);
    res.status(500).json({ error: "Internal server error" });
  }
};



export const markMessagesAsRead = async (req, res) => {
  try {
    const myId = req.user._id;
    const { id: senderId } = req.params;

    await Message.updateMany(
      {
        senderId,
        receiverId: myId,
        isRead: false,
      },
      { $set: { isRead: true } }
    );

    res.status(200).json({ success: true });
  } catch (error) {
    console.log("markMessagesAsRead error:", error.message);
    res.status(500).json({ error: "Internal server error" });
  }
};


export const deleteChat = async (req, res) => {
  try {
    const myId = req.user._id;
    const { id: otherUserId } = req.params;

    await Message.updateMany(
      {
        $or: [
          { senderId: myId, receiverId: otherUserId },
          { senderId: otherUserId, receiverId: myId },
        ],
      },
      {
        $addToSet: { deletedFor: myId },
      }
    );

    res.status(200).json({ success: true });
  } catch (error) {
    console.error("Delete chat error:", error.message);
    res.status(500).json({ error: "Internal server error" });
  }
};
