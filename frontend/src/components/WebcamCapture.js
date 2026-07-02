import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

function WebcamCapture({ onResult }) {
  const webcamRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/predict_face`, { image: imageSrc });
      setLoading(false);
      onResult(res.data);
    } catch (err) {
      setLoading(false);
      alert("Error analyzing face emotion.");
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={320}
        height={240}
      />
      <button onClick={capture} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Emotion"}
      </button>
    </div>
  );
}

export default WebcamCapture;
