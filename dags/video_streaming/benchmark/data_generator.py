from pathlib import Path
import json
import csv
import random
import logging


def generate_data(n: int, data_dir: Path):
    """
    Generate CSV and JSON files with n records.
    CSV: Flat with hobbies as comma-separated string.
    JSON: With hobbies as list for nesting (mejor para MongoDB).
    
    Incluye más variedad en los datos para hacer pruebas más realistas.
    """
    logging.info(f"Generating {n} records...")
    
    csv_path = data_dir / 'data.csv'
    json_path = data_dir / 'data.json'
    
    # Datos más diversos para pruebas realistas
    cities = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
    ]
    
    hobbies_options = [
        'reading', 'sports', 'music', 'travel', 'cooking',
        'photography', 'gaming', 'hiking', 'painting', 'dancing',
        'yoga', 'cycling', 'swimming', 'gardening', 'writing'
    ]
    
    first_names = [
        'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer',
        'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
        'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah',
        'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
        'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez',
        'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor'
    ]
    
    try:
        # Generate CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'age', 'city', 'hobbies'])
            
            for i in range(1, n + 1):
                # Nombres más realistas
                full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                
                # Edad con distribución más realista (más personas entre 25-45)
                # Rango: 18-70 (53 valores)
                age_range = list(range(18, 71))
                # Crear pesos: menos peso a extremos, más peso al centro
                weights = []
                for age in age_range:
                    if 25 <= age <= 45:
                        weights.append(3)  # Más probable
                    elif 20 <= age <= 50:
                        weights.append(2)  # Probable
                    else:
                        weights.append(1)  # Menos probable
                
                age = random.choices(age_range, weights=weights, k=1)[0]
                
                # Hobbies: personas mayores tienden a tener menos hobbies
                num_hobbies = random.randint(1, max(1, 6 - (age // 15)))
                hobbies_str = ','.join(random.sample(hobbies_options, num_hobbies))
                
                city = random.choice(cities)
                
                writer.writerow([i, full_name, age, city, hobbies_str])
        
        # Generate JSON
        data = []
        for i in range(1, n + 1):
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Misma distribución de edad
            age_range = list(range(18, 71))
            weights = []
            for age in age_range:
                if 25 <= age <= 45:
                    weights.append(3)
                elif 20 <= age <= 50:
                    weights.append(2)
                else:
                    weights.append(1)
            
            age = random.choices(age_range, weights=weights, k=1)[0]
            
            num_hobbies = random.randint(1, max(1, 6 - (age // 15)))
            hobbies_list = random.sample(hobbies_options, num_hobbies)
            
            city = random.choice(cities)
            
            # JSON con estructura más rica (ventaja para NoSQL)
            doc = {
                'id': i,
                'name': full_name,
                'age': age,
                'city': city,
                'hobbies': hobbies_list,  # Array nativo
                'metadata': {  # Objeto anidado adicional
                    'created_year': random.randint(2020, 2024),
                    'active': random.choice([True, False]),
                    'score': round(random.uniform(1.0, 10.0), 2)
                }
            }
            data.append(doc)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logging.info("Data generation completed successfully.")
        
    except Exception as e:
        logging.error(f"Error generating data: {e}")
        raise
    
    return csv_path, json_path