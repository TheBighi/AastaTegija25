from flask import Flask, render_template, request, jsonify
import csv
import random
import os

app = Flask(__name__, static_folder='static')

def load_cars_data():
    cars = []
    try:
        with open('autod_maksudega.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            headers = next(reader)
            for row in reader:
                if len(row) >= 48:  # Make sure the row has all columns
                    car = {
                        'mark': row[0],
                        'mudel': row[1],
                        'esmane_reg': row[4],
                        'varv': row[10],
                        'mootori_maht': row[24],
                        'mootori_voimsus': row[25],
                        'kytuse_tyyp': row[30],
                        'aastamaks': row[46],
                        'registreerimistasu': row[47]
                    }
                    
                    # Only add cars with valid tax information
                    if car['aastamaks'] and car['registreerimistasu']:
                        try:
                            car['aastamaks'] = float(car['aastamaks'].replace(',', '.'))
                            car['registreerimistasu'] = float(car['registreerimistasu'].replace(',', '.'))
                            cars.append(car)
                        except ValueError:
                            pass
            
    except Exception as e:
        print(f"Error loading data: {e}")
    
    return cars

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/get_car_options', methods=['GET'])
def get_car_options():
    cars = load_cars_data()
    
    if not cars or len(cars) < 2:
        return jsonify({'error': 'Not enough car data available'}), 400
    
    # Select two random cars
    chosen_cars = random.sample(cars, 2)
    
    # Randomly select which car has the target tax values
    correct_index = random.randint(0, 1)
    target_car = chosen_cars[correct_index]
    
    return jsonify({
        'cars': [
            {
                'mark': car['mark'],
                'mudel': car['mudel'],
                'esmane_reg': car['esmane_reg'],
                'varv': car['varv'],
                'mootori_maht': car['mootori_maht'],
                'mootori_voimsus': car['mootori_voimsus'],
                'kytuse_tyyp': car['kytuse_tyyp']
            } for car in chosen_cars
        ],
        'target': {
            'aastamaks': target_car['aastamaks'],
            'registreerimistasu': target_car['registreerimistasu']
        },
        'correct_index': correct_index
    })

@app.route('/find_cars_by_tax', methods=['GET'])
def find_cars_by_tax():
    aastamaks = float(request.args.get('aastamaks', 0))
    tax_range = float(request.args.get('range', 10))
    
    if aastamaks < 0:
        return jsonify({'error': 'Aastamaks peab olema positiivne number'}), 400
    
    cars = load_cars_data()
    
    if not cars:
        return jsonify({'error': 'No car data available'}), 400
    
    # Find cars within the tax range
    min_tax = aastamaks - tax_range
    max_tax = aastamaks + tax_range
    
    matching_cars = [car for car in cars if min_tax <= car['aastamaks'] <= max_tax]
    
    # Limit to 20 results to avoid overwhelming the UI
    if len(matching_cars) > 20:
        matching_cars = random.sample(matching_cars, 20)
    
    # Sort by how close they are to the target tax
    matching_cars.sort(key=lambda car: abs(car['aastamaks'] - aastamaks))
    
    return jsonify({
        'count': len(matching_cars),
        'target_tax': aastamaks,
        'cars': [
            {
                'mark': car['mark'],
                'mudel': car['mudel'],
                'esmane_reg': car['esmane_reg'],
                'varv': car['varv'],
                'mootori_maht': car['mootori_maht'],
                'mootori_voimsus': car['mootori_voimsus'],
                'kytuse_tyyp': car['kytuse_tyyp'],
                'aastamaks': car['aastamaks'],
                'registreerimistasu': car['registreerimistasu']
            } for car in matching_cars
        ]
    })
@app.route('/taxes')
def taxes():
    return render_template('taxes.html')

@app.route('/get_brands')
def get_brands():
    cars = load_cars_data()
    brands = sorted(set(car['mark'] for car in cars))
    return jsonify(brands)

@app.route('/get_models')
def get_models():
    mark = request.args.get('mark')
    cars = load_cars_data()
    models = sorted(set(car['mudel'] for car in cars if car['mark'] == mark))
    return jsonify(models)

@app.route('/get_taxes')
def get_taxes():
    mark = request.args.get('mark')
    mudel = request.args.get('mudel')
    aasta = request.args.get('aasta')

    cars = load_cars_data()
    filtered_cars = [car for car in cars if car['mark'] == mark and car['mudel'] == mudel]
    
    if aasta:
        filtered_cars = [car for car in filtered_cars if car['esmane_reg'] == aasta]

    if not filtered_cars:
        return jsonify({'error': 'Andmeid ei leitud'}), 404

    avg_aastamaks = sum(car['aastamaks'] for car in filtered_cars) / len(filtered_cars)
    avg_regtasu = sum(car['registreerimistasu'] for car in filtered_cars) / len(filtered_cars)
    
    # Get a sample car to display
    sample_car = filtered_cars[0]
    
    return jsonify({
        'aastamaks': round(avg_aastamaks, 2),
        'regtasu': round(avg_regtasu, 2),
        'sample_car': {
            'mark': sample_car['mark'],
            'mudel': sample_car['mudel'],
            'esmane_reg': sample_car['esmane_reg'],
            'varv': sample_car['varv'],
            'mootori_maht': sample_car['mootori_maht'] + " cm³",
            'mootori_voimsus': sample_car['mootori_voimsus'] + " kW",
            'kytuse_tyyp': sample_car['kytuse_tyyp']
        }
    })

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/analyze_tax', methods=['GET'])
def analyze_tax():
    aastamaks = float(request.args.get('aastamaks', 0))
    
    if aastamaks <= 0:
        return jsonify({'error': 'Aastamaks peab olema positiivne number'}), 400
    
    cars = load_cars_data()
    
    if not cars:
        return jsonify({'error': 'No car data available'}), 400
    
    # Calculate statistics
    higher_count = sum(1 for car in cars if car['aastamaks'] > aastamaks)
    lower_count = sum(1 for car in cars if car['aastamaks'] <= aastamaks)
    total_count = higher_count + lower_count
    
    higher_percentage = round((higher_count / total_count) * 100)
    lower_percentage = round((lower_count / total_count) * 100)
    
    average_tax = sum(car['aastamaks'] for car in cars) / len(cars)
    is_below_average = aastamaks < average_tax
    
    # Find similar cars
    similar_cars = []
    tax_range = 10  # Range in euros to find similar cars
    
    matching_cars = [car for car in cars if abs(car['aastamaks'] - aastamaks) <= tax_range]
    
    # Limit to 3 results
    if len(matching_cars) > 3:
        matching_cars = sorted(matching_cars, key=lambda car: abs(car['aastamaks'] - aastamaks))[:3]
    
    return jsonify({
        'higher_count': higher_count,
        'lower_count': lower_count,
        'higher_percentage': higher_percentage,
        'lower_percentage': lower_percentage,
        'average_tax': round(average_tax, 2),
        'is_below_average': is_below_average,
        'similar_cars': [
            {
                'mark': car['mark'],
                'mudel': car['mudel'],
                'esmane_reg': car['esmane_reg'],
                'mootori_voimsus': car['mootori_voimsus'],
                'kytuse_tyyp': car['kytuse_tyyp'],
                'aastamaks': round(car['aastamaks'], 2),
                'registreerimistasu': round(car['registreerimistasu'], 2)
            } for car in matching_cars
        ]
    })

@app.route('/analyze_reg_fee', methods=['GET'])
def analyze_reg_fee():
    regtasu = float(request.args.get('regtasu', 0))
    
    if regtasu <= 0:
        return jsonify({'error': 'Registreerimistasu peab olema positiivne number'}), 400
    
    cars = load_cars_data()
    
    if not cars:
        return jsonify({'error': 'No car data available'}), 400
    
    # Calculate statistics
    higher_count = sum(1 for car in cars if car['registreerimistasu'] > regtasu)
    lower_count = sum(1 for car in cars if car['registreerimistasu'] <= regtasu)
    total_count = higher_count + lower_count
    
    higher_percentage = round((higher_count / total_count) * 100)
    lower_percentage = round((lower_count / total_count) * 100)
    
    average_reg = sum(car['registreerimistasu'] for car in cars) / len(cars)
    is_below_average = regtasu < average_reg
    
    # Find similar cars
    similar_cars = []
    reg_range = 50  # Range in euros to find similar cars
    
    matching_cars = [car for car in cars if abs(car['registreerimistasu'] - regtasu) <= reg_range]
    
    # Limit to 3 results
    if len(matching_cars) > 3:
        matching_cars = sorted(matching_cars, key=lambda car: abs(car['registreerimistasu'] - regtasu))[:3]
    
    return jsonify({
        'higher_count': higher_count,
        'lower_count': lower_count,
        'higher_percentage': higher_percentage,
        'lower_percentage': lower_percentage,
        'average_reg': round(average_reg, 2),
        'is_below_average': is_below_average,
        'similar_cars': [
            {
                'mark': car['mark'],
                'mudel': car['mudel'],
                'esmane_reg': car['esmane_reg'],
                'mootori_voimsus': car['mootori_voimsus'],
                'kytuse_tyyp': car['kytuse_tyyp'],
                'aastamaks': round(car['aastamaks'], 2),
                'registreerimistasu': round(car['registreerimistasu'], 2)
            } for car in matching_cars
        ]
    })
@app.route('/find_cars_by_regtasu', methods=['GET'])
def find_cars_by_regtasu():
    regtasu = float(request.args.get('regtasu', 0))
    tax_range = float(request.args.get('range', 50))
    
    if regtasu < 0:
        return jsonify({'error': 'Registreerimistasu peab olema positiivne number'}), 400
    
    cars = load_cars_data()
    
    if not cars:
        return jsonify({'error': 'No car data available'}), 400
    
    # Find cars within the registration fee range
    min_fee = regtasu - tax_range
    max_fee = regtasu + tax_range
    
    matching_cars = [car for car in cars if min_fee <= car['registreerimistasu'] <= max_fee]
    
    # Limit to 20 results to avoid overwhelming the UI
    if len(matching_cars) > 20:
        matching_cars = random.sample(matching_cars, 20)
    
    # Sort by how close they are to the target fee
    matching_cars.sort(key=lambda car: abs(car['registreerimistasu'] - regtasu))
    
    return jsonify({
        'count': len(matching_cars),
        'target_fee': regtasu,
        'cars': [
            {
                'mark': car['mark'],
                'mudel': car['mudel'],
                'esmane_reg': car['esmane_reg'],
                'varv': car['varv'],
                'mootori_maht': car['mootori_maht'],
                'mootori_voimsus': car['mootori_voimsus'],
                'kytuse_tyyp': car['kytuse_tyyp'],
                'aastamaks': car['aastamaks'],
                'registreerimistasu': car['registreerimistasu']
            } for car in matching_cars
        ]
    })
if __name__ == '__main__':
    app.run(debug=True, port=8080)