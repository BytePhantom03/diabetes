from flask import Flask, request, jsonify
import torch
import numpy as np
import joblib
from model import DiabetesModel
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load model
model = DiabetesModel()
model.load_state_dict(torch.load("model.pth"))
model.eval()

# Load scaler
scaler = joblib.load("scaler.pkl")

@app.route("/")
def home():
    return "API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    
    input_data = np.array([[
        data["pregnancies"],
        data["glucose"],
        data["bp"],
        data["skin"],
        data["insulin"],
        data["bmi"],
        data["dpf"],
        data["age"]
    ]])
    
    input_data = scaler.transform(input_data)
    input_data = torch.FloatTensor(input_data)
    
    prediction = model(input_data).item()
    
    result = "Diabetic" if prediction > 0.5 else "Not Diabetic"
    
    return jsonify({
        "prediction": result,
        "probability": float(prediction)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))