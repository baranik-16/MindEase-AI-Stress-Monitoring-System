import React, { useState, useRef } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import { useNavigate } from "react-router-dom";

const API_BASE = process.env.REACT_APP_API_URL;

function Dashboard() {
  const [mode, setMode] = useState("text"); // text | webcam | both
  const [emotion, setEmotion] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [webcamEmotion, setWebcamEmotion] = useState(null);
  const webcamRef = useRef(null);
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  const captureAndPredictEmotion = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const res = await axios.post(`${API_BASE}/predict_face`, { image: imageSrc });
    setWebcamEmotion(res.data);
    return res.data.emotion;
  };

  const handlePredict = async () => {
    try {
      let finalEmotion = emotion;

      if (mode === "webcam" || mode === "both") {
        const faceResult = await captureAndPredictEmotion();
        finalEmotion = faceResult;
      }

      const payload = {
        username,
        emotion: finalEmotion,
        text: mode !== "webcam" ? text : "",
      };

      const res = await axios.post(`${API_BASE}/predict`, payload);
      setResult(res.data);
    } catch (err) {
      alert("Error predicting stress.");
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("username");
    navigate("/");
  };

  return (
    <div className="container">
      <h2>Welcome, {username} 👋</h2>

      <div>
        <label>Select Input Mode: </label>
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="text">Text</option>
          <option value="webcam">Webcam</option>
          <option value="both">Both</option>
        </select>
      </div>

      {mode !== "webcam" && (
        <textarea
          placeholder="Type your thoughts here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      )}

      {(mode === "webcam" || mode === "both") && (
        <div className="webcam-container">
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={320}
            height={240}
            mirrored
          />
          <button onClick={captureAndPredictEmotion}>Capture Emotion</button>
          {webcamEmotion && <p>Detected Emotion: {webcamEmotion.emotion}</p>}
        </div>
      )}

      <button onClick={handlePredict}>Predict Stress</button>
      <button
        onClick={handleLogout}
        style={{ background: "#dc3545", marginTop: "10px" }}
      >
        Logout
      </button>

      {result && (
        <div className="result-box">
          <h3>Predicted Stress Level: {result.predicted_stress_level}</h3>
          <p>Confidence: {result.confidence}</p>
          <div className="suggestions">
            <b>Suggestions:</b>
            <ul>
              {(result.suggestions || []).map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
