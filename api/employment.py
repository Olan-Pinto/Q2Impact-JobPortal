from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Mock data for employment sectors
@app.route('/api/employment', methods=['GET'])
def get_employment_data():
    data = {
        "sectors": ["Agriculture", "Manufacturing", "Services", "IT", "Education", "Health"],
        "counts": [random.randint(100, 500) for _ in range(6)] 
    }
    return jsonify(data)

# Mock data for economic sectors distribution
@app.route('/api/economic_sectors', methods=['GET'])
def get_economic_sectors():
    data = {
        "sectors": ["Agriculture", "Industry", "Services"],
        "percentages": [20, 30, 50]  # Example data showing distribution percentages
    }
    return jsonify(data)

# Mock data for position types
@app.route('/api/position_types', methods=['GET'])
def get_position_types():
    data = {
        "types": ["Full-time", "Part-time", "Freelance"],
        "counts": [50, 30, 20]  # Example count of positions for each type
    }
    return jsonify(data)

# Mock data for vacancies by governorate
@app.route('/api/vacancies', methods=['GET'])
def get_vacancies():
    data = {
        "governorates": ["Amman", "Irbid", "Zarqa", "Aqaba", "Mafraq"],
        "counts": [random.randint(10, 50) for _ in range(5)]  # Random vacancy counts for each governorate
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)