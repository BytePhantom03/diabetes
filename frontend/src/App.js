import React, { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    pregnancies: "",
    glucose: "",
    bp: "",
    skin: "",
    insulin: "",
    bmi: "",
    dpf: "",
    age: "",
  });

  const [result, setResult] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await axios.post("http://127.0.0.1:5000/predict", form);
    setResult(
      res.data.prediction + " (Prob: " + res.data.probability.toFixed(2) + ")",
    );
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Diabetes Prediction</h1>

      {Object.keys(form).map((key) => (
        <input key={key} name={key} placeholder={key} onChange={handleChange} />
      ))}

      <br />
      <br />
      <button onClick={handleSubmit}>Predict</button>

      <h2>{result}</h2>
    </div>
  );
}

export default App;
