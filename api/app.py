from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# List of valid measure names
VALID_MEASURES = [
    'Violent crime rate',
    'Unemployment',
    'Children in poverty',
    'Diabetic screening',
    'Mammography screening',
    'Preventable hospital stays',
    'Uninsured',
    'Sexually transmitted infections',
    'Physical inactivity',
    'Adult obesity',
    'Premature Death',
    'Daily fine particulate matter'
]

def get_db_connection():
    if app.config.get('TESTING'):
        db_path = app.config['DATABASE']
    else:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/county_data', methods=['POST'])
def county_data():
    # Get JSON data from request
    data = request.get_json()
    
    # Check for teapot easter egg
    if data.get('coffee') == 'teapot':
        return '', 418
    
    # Validate required fields
    zip_code = data.get('zip')
    measure_name = data.get('measure_name')
    
    if not zip_code or not measure_name:
        return jsonify({'error': 'Both zip and measure_name are required'}), 400
    
    # Validate zip code format
    if not (len(zip_code) == 5 and zip_code.isdigit()):
        return jsonify({'error': 'Invalid zip code format'}), 400
    
    # Validate measure name
    if measure_name not in VALID_MEASURES:
        return jsonify({'error': 'Invalid measure_name'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to join zip_county and county_health_rankings tables
        query = """
        SELECT chr.*
        FROM zip_county zc
        JOIN county_health_rankings chr ON zc.county_code = chr.fipscode
        WHERE zc.zip = ? AND chr.measure_name = ?
        """
        
        cursor.execute(query, (zip_code, measure_name))
        result = cursor.fetchall()
        
        if result is None:
            return jsonify({'error': 'No data found for given zip and measure_name'}), 404
        
        # Convert results to list of dictionaries
        output = []
        for row in result:
            output.append(dict(row))
        
        conn.close()
        return jsonify(output)
    
    except Exception as e:
        app.logger.error(f'Error in county_data: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
