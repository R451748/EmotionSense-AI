import axios from "axios";

const API_URL = "http://localhost:5050";

export const detectEmotion = async (formData) => {
  try {
    if (formData.has("file")) {
      const file = formData.get("file");
      const ext = file.name.split(".").pop().toLowerCase();

      let endpoint = "/predict/facial";
      if (["wav", "mp3"].includes(ext)) endpoint = "/predict/voice";

      const res = await axios.post(`${API_URL}${endpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res;
    } else if (formData.has("text")) {
      const text = formData.get("text");
      const res = await axios.post(
        `${API_URL}/predict/text`,
        { text },
        { headers: { "Content-Type": "application/json" } }
      );
      return res;
    } else {
      throw new Error("No input provided");
    }
  } catch (error) {
    console.error("❌ API Error:", error);
    throw error;
  }
};
