import json
import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the model and scaler
regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scaling = pickle.load(open('scaling.pkl', 'rb'))  # Ensure 'scaling.pkl' exists

@app.route("/")
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    """
    Predict API route for JSON input.
    Expects a JSON payload with a 'data' key containing input features.
    """
    try:
        # Validate and parse JSON data
        if not request.is_json:
            return jsonify({'error': 'Invalid input: Expected JSON payload.'}), 400
        
        data = request.json.get('data')
        if not data:
            return jsonify({'error': "Missing 'data' key in JSON payload."}), 400

        print("Received data:", data)

        # Convert input to numpy array and scale
        new_data = scaling.transform(np.array(list(data.values())).reshape(1, -1))
        print("Transformed input data:", new_data)

        # Predict using the model
        output = regmodel.predict(new_data)
        print("Prediction:", output[0])

        # Return prediction
        return jsonify({'prediction': float(output[0])})
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Web form-based prediction route.
    Accepts input features from an HTML form.
    """
    try:
        # Retrieve and process form data
        data = [float(x) for x in request.form.values()]
        print("Received form data:", data)

        # Convert input data to numpy array and scale
        final_input = scaling.transform(np.array(data).reshape(1, -1))
        print("Transformed input data:", final_input)

        # Predict using the model
        output = regmodel.predict(final_input)[0]
        print("Prediction:", output)

        # Render result on the home page
        return render_template("home.html", prediction_text=f"The House Price Prediction is {output}")
    except Exception as e:
        print("Error occurred:", str(e))
        return render_template("home.html", error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
