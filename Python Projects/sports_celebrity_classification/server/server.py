from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/classify_image', methods=['POST'])
def classify_image():
    try:
        # Support both form-data and JSON requests
        if request.is_json:
            image_data = request.get_json().get('image_data')
        else:
            image_data = request.form.get('image_data')

        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        print("Received Image Data for Classification")
        
        response_data = util.classify_image(image_data)
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', '*')

        print("Response:", response_data)
        return response

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    app.run(port=5000, debug=True)
