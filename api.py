from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data = {"message" : "Sample Test"}

# Get endpoint - Testing
@app.route('/api/get-data', methods = ['GET'])
def get_data():
    return jsonify(data), 200

# Post endpoint - Testing
@app.route('/api/post-data', methods = ['POST'])
def post_data():
    incoming_data = request.json
    print("Recieved data: ", incoming_data)
    response = {"message": "Data recieved successfully", "recieved_data" : incoming_data}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug = True)