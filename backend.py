from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# List of districts in Tamil Nadu that might be affected by floods
districts = [
    "சென்னை (Chennai)",
    "கடலூர் (Cuddalore)",
    "நாகப்பட்டினம் (Nagapattinam)",
    "திருவாரூர் (Thiruvarur)",
    "தஞ்சாவூர் (Thanjavur)",
    "விழுப்புரம் (Viluppuram)",
    "காஞ்சிபுரம் (Kanchipuram)",
    "திருவள்ளூர் (Tiruvallur)"
]

def generate_flood_data():
    """Generate random flood data for districts"""
    data = {}
    for district in districts:
        # Random number of affected persons (between 0 and 10000)
        affected_persons = random.randint(0, 10000)
        # Random area in square kilometers (between 0 and 500)
        affected_area = random.randint(0, 500)
        data[district] = {
            "affected_persons": affected_persons,
            "area_sqkm": affected_area
        }
    return data

@app.route('/')
def home():
    return render_template('flood.html')

@app.route('/flood_data')
def flood_data():
    data = generate_flood_data()
    return jsonify(data)

# HTML template as a string (will be used by render_template)
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>தமிழ்நாடு வெள்ள பாதிப்பு தகவல்</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .timestamp {
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <h2>தமிழ்நாடு வெள்ள பாதிப்பு தகவல் (Flood Affected Areas in Tamil Nadu)</h2>
    <table id="floodTable">
        <tr>
            <th>மாவட்டம் (District)</th>
            <th>பாதிக்கப்பட்ட மக்கள் (Affected Persons)</th>
            <th>பாதிக்கப்பட்ட பரப்பளவு (சதுர கி.மீ) (Area in sq.km)</th>
        </tr>
    </table>
    <div class="timestamp" id="timestamp"></div>

    <script>
        function updateData() {
            fetch('/flood_data')
                .then(response => response.json())
                .then(data => {
                    let table = document.getElementById('floodTable');
                    // Clear existing rows (except header)
                    while(table.rows.length > 1) {
                        table.deleteRow(1);
                    }
                    
                    // Add new data
                    for (let district in data) {
                        let row = table.insertRow();
                        let cell1 = row.insertCell(0);
                        let cell2 = row.insertCell(1);
                        let cell3 = row.insertCell(2);
                        
                        cell1.innerHTML = district;
                        cell2.innerHTML = data[district].affected_persons;
                        cell3.innerHTML = data[district].area_sqkm;
                    }
                    
                    // Update timestamp
                    document.getElementById('timestamp').innerHTML = 
                        'கடைசியாக புதுப்பிக்கப்பட்டது: ' + new Date().toLocaleString();
                });
        }

        // Initial load
        updateData();
        // Refresh every 30 seconds
        setInterval(updateData, 30000);
    </script>
</body>
</html>
'''

# Create the template file dynamically
import os
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(template_dir, exist_ok=True)
with open(os.path.join(template_dir, 'flood.html'), 'w', encoding='utf-8') as f:
    f.write(html_template)

if __name__ == '__main__':
    app.run(debug=True)