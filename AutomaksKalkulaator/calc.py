import csv
import datetime
from datetime import date
import math
import os

def read_csv(file_path):
    """Read data from CSV file with semicolon delimiter."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            headers = next(reader)
            for row in reader:
                data.append(dict(zip(headers, row)))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return [], []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return [], []
    
    return headers, data

def round_value(n, dec):
    """Round a number to specified decimal places."""
    x = n * (10 ** dec)
    x = round(x)
    return x / (10 ** dec)

def parse_date(date_str):
    """Parse date from string format."""
    if not date_str:
        return None
    
    try:
        # Try common formats
        for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y.%m.%d'):
            try:
                return datetime.datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        print(f"Warning: Could not parse date '{date_str}'")
        return None
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

def calculate_age_multiplier(years_since_reg):
    """Calculate age multiplier based on vehicle age."""
    if years_since_reg >= 20:
        return 0
    elif years_since_reg >= 15:
        return 0.1
    elif years_since_reg >= 14:
        return 0.18
    elif years_since_reg >= 13:
        return 0.26
    elif years_since_reg >= 12:
        return 0.35
    elif years_since_reg >= 11:
        return 0.43
    elif years_since_reg >= 10:
        return 0.51
    elif years_since_reg >= 9:
        return 0.59
    elif years_since_reg >= 8:
        return 0.67
    elif years_since_reg >= 7:
        return 0.75
    elif years_since_reg >= 6:
        return 0.84
    elif years_since_reg >= 5:
        return 0.92
    else:
        return 1

def calculate_reg_fee_multiplier(years_since_reg):
    """Calculate registration fee multiplier based on vehicle age."""
    if years_since_reg >= 20:
        return 0.05
    elif years_since_reg >= 19:
        return 0.06
    elif years_since_reg >= 18:
        return 0.07
    elif years_since_reg >= 17:
        return 0.08
    elif years_since_reg >= 16:
        return 0.09
    elif years_since_reg >= 15:
        return 0.10
    elif years_since_reg >= 14:
        return 0.12
    elif years_since_reg >= 13:
        return 0.14
    elif years_since_reg >= 12:
        return 0.16
    elif years_since_reg >= 11:
        return 0.19
    elif years_since_reg >= 10:
        return 0.22
    elif years_since_reg >= 9:
        return 0.26
    elif years_since_reg >= 8:
        return 0.31
    elif years_since_reg >= 7:
        return 0.36
    elif years_since_reg >= 6:
        return 0.42
    elif years_since_reg >= 5:
        return 0.48
    elif years_since_reg >= 4:
        return 0.56
    elif years_since_reg >= 3:
        return 0.65
    elif years_since_reg >= 2:
        return 0.75
    elif years_since_reg >= 1:
        return 0.87
    else:
        return 1

def get_vehicle_type(kategooria, alamkategooria, kere_nimetus):
    """Determine vehicle type from category information."""
    if kategooria in ['M1', 'M1G']:
        return 'M1_M1G'
    elif kategooria in ['N1', 'N1G']:
        return 'N1_N1G'
    elif kategooria in ['L3e', 'L4e', 'L5e', 'L6e', 'L7e']:
        return 'L3e_L4e_L5e_L6e_L7e'
    elif kategooria == 'MS2':
        return 'MS2'
    elif kategooria in ['T1b', 'T5']:
        return 'T1b_T5'
    elif kategooria == 'T3':
        return 'T3'
    else:
        return 'OTHER'

def determine_is_house(kere_nimetus):
    """Determine if the vehicle is a house vehicle (camper)."""
    keywords = ['autoelamu', 'camper', 'motorhome', 'house']
    for keyword in keywords:
        if keyword.lower() in str(kere_nimetus).lower():
            return 'Yes'
    return 'No'

def get_general_engine_type(mootori_tyyp, hybriidi_tyyp):
    """Determine general engine type from engine info."""
    if mootori_tyyp == 'ELEKTER':
        return 'ELECTRIC'
    elif hybriidi_tyyp == 'NOVC-HEV':
        return 'NOVC-HEV'
    elif hybriidi_tyyp == 'OVC-HEV':
        return 'OVC-HEV'
    else:
        return 'ICE'  # Internal Combustion Engine

def get_fuel_type(kytuse_tyyp):
    """Get standardized fuel type."""
    if 'DIISEL' in str(kytuse_tyyp).upper():
        return 'diesel'
    elif 'BENSIIN' in str(kytuse_tyyp).upper() or 'PETROL' in str(kytuse_tyyp).upper():
        return 'petrol'
    else:
        return 'other'

def get_co2_standard(co2_nedc, co2_wltp):
    """Determine CO2 standard based on available data."""
    if co2_wltp and co2_wltp.strip():
        return 'WLTP'
    elif co2_nedc and co2_nedc.strip():
        return 'NEDC'
    else:
        return 'Not_available'

def get_co2_emission(co2_standard, co2_nedc, co2_wltp):
    """Get CO2 emission value based on standard."""
    if co2_standard == 'WLTP' and co2_wltp:
        try:
            return float(co2_wltp.replace(',', '.'))
        except (ValueError, TypeError):
            return 0
    elif co2_standard == 'NEDC' and co2_nedc:
        try:
            return float(co2_nedc.replace(',', '.'))
        except (ValueError, TypeError):
            return 0
    return 0

def calculate_car_tax(vehicle):
    """Calculate car tax and registration fee for a vehicle."""
    # Extract vehicle data
    try:
        # Extract and convert needed values
        try:
            kerb_mass = float(vehicle.get('TYHIMASS', '0').replace(',', '.'))
        except (ValueError, TypeError):
            kerb_mass = 0
            
        try:
            max_net_power = float(vehicle.get('MOOTORI_VOIMSUS', '0').replace(',', '.'))
        except (ValueError, TypeError):
            max_net_power = 0
            
        try:
            gross_weight = float(vehicle.get('TAISMASS', '0').replace(',', '.'))
        except (ValueError, TypeError):
            gross_weight = 0
            
        try:
            engine_capacity = float(vehicle.get('MOOTORI_MAHT', '0').replace(',', '.'))
        except (ValueError, TypeError):
            engine_capacity = 0
        
        # Determine vehicle classification
        vehicle_type = get_vehicle_type(vehicle.get('KATEGOORIA', ''), 
                                       vehicle.get('ALAMKATEGOORIA', ''),
                                       vehicle.get('KERE_NIMETUS', ''))
        
        is_house = determine_is_house(vehicle.get('KERE_NIMETUS', ''))
        
        # Engine/fuel information
        general_engine_type = get_general_engine_type(vehicle.get('MOOTORI_TYYP', ''),
                                                    vehicle.get('HYBRIIDI_TYYP', ''))
        
        fuel_type = get_fuel_type(vehicle.get('KYTUSE_TYYP', ''))
        
        # CO2 information
        co2_standard = get_co2_standard(vehicle.get('CO2_NEDC', ''), vehicle.get('CO2_WLTP', ''))
        
        # Date information
        reg_date = parse_date(vehicle.get('ESMANE_REG', ''))
        if not reg_date:
            reg_date = parse_date(vehicle.get('EESTIS_ESMAREG', ''))
            
        if not reg_date:
            # Default to 10 years old if no date
            years_since_reg = 10
        else:
            beginning_of_tax_period = date(date.today().year + 1, 1, 1)
            years_since_reg = (beginning_of_tax_period - reg_date).days / 365.25
        
        # Calculate emission coefficient
        emission_coefficient = 1
        if co2_standard == 'NEDC':
            if (vehicle_type == 'M1_M1G' and is_house == 'No') or (vehicle_type == 'N1_N1G' and (max_net_power / kerb_mass > 0.20)):
                emission_coefficient = 1.21
            elif (vehicle_type == 'N1_N1G' and (max_net_power / kerb_mass <= 0.20)) or (vehicle_type == 'M1_M1G' and is_house == 'Yes'):
                emission_coefficient = 1.30
        
        # Calculate CO2 emission
        if co2_standard == 'Not_available':
            if (vehicle_type == 'M1_M1G' and is_house == 'No') or (vehicle_type == 'N1_N1G' and (max_net_power / kerb_mass > 0.20)):
                co2_emission = round_value((max_net_power * 0.29) + (kerb_mass * 0.07) + (years_since_reg * 4.92), 0)
                
                if fuel_type == 'diesel' and general_engine_type == 'NOVC-HEV':
                    co2_emission -= 52
                elif fuel_type == 'diesel' and (general_engine_type != 'NOVC-HEV' and general_engine_type != 'OVC-HEV'):
                    co2_emission -= 35
                elif fuel_type == 'petrol' and general_engine_type == 'NOVC-HEV':
                    co2_emission -= 39
                elif general_engine_type == 'OVC-HEV':
                    co2_emission = 0
            elif (vehicle_type == 'N1_N1G' and (max_net_power / kerb_mass <= 0.20)) or (vehicle_type == 'M1_M1G' and is_house == 'Yes'):
                co2_emission = round_value((max_net_power * 0.40) + (kerb_mass * 0.07) + (years_since_reg * 5.16), 0)
                
                if fuel_type == 'petrol' and (general_engine_type != 'NOVC-HEV' and general_engine_type != 'OVC-HEV'):
                    co2_emission += 22
                elif fuel_type == 'diesel' and general_engine_type == 'NOVC-HEV':
                    co2_emission -= 20
                elif fuel_type == 'petrol' and general_engine_type == 'NOVC-HEV':
                    co2_emission -= 20
                elif general_engine_type == 'OVC-HEV':
                    co2_emission = 0
                    
            co2_emission = min(co2_emission, 350)
        else:
            co2_emission = get_co2_emission(co2_standard, vehicle.get('CO2_NEDC', ''), vehicle.get('CO2_WLTP', '')) * emission_coefficient * 1
        
        # Calculate multipliers
        age_multiplier = calculate_age_multiplier(years_since_reg)
        reg_fee_multiplier = calculate_reg_fee_multiplier(years_since_reg)
        
        # Initialize tax values
        base_tax = 0
        co2_tax = 0
        weight_tax = 0
        reg_base_fee = 0
        reg_co2_fee = 0
        reg_weight_fee = 0
        
        # Calculate tax based on vehicle type
        if ((vehicle_type == 'L3e_L4e_L5e_L6e_L7e' or 
            (vehicle_type == 'MS2' and kerb_mass <= 1000) or 
            (vehicle_type == 'T1b_T5' and kerb_mass <= 1000) or 
            vehicle_type == 'T3') and general_engine_type != 'ELECTRIC'):
            
            if years_since_reg <= 10:
                if 51 <= engine_capacity <= 125:
                    base_tax = 30
                elif 126 <= engine_capacity <= 500:
                    base_tax = 45
                elif 501 <= engine_capacity <= 1000:
                    base_tax = 60
                elif 1001 <= engine_capacity <= 1500:
                    base_tax = 75
                elif engine_capacity > 1500:
                    base_tax = 90
            elif 10 < years_since_reg <= 20:
                if 126 <= engine_capacity <= 500:
                    base_tax = 30
                elif 501 <= engine_capacity <= 1000:
                    base_tax = 45
                elif 1001 <= engine_capacity <= 1500:
                    base_tax = 60
                elif engine_capacity > 1500:
                    base_tax = 75
        
        elif (vehicle_type == 'M1_M1G' and is_house == 'No') or (vehicle_type == 'N1_N1G' and (max_net_power / kerb_mass > 0.20)):
            base_tax = 50
            reg_base_fee = 150
            
            if general_engine_type != 'ELECTRIC':
                if co2_emission < 118:
                    co2_tax = 0
                    reg_co2_fee = 46*5 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * (co2_emission * 5), 2)
                elif 118 <= co2_emission <= 150:
                    co2_tax = round_value(age_multiplier * ((co2_emission - 117) * 3), 2)
                    reg_co2_fee = 46*5 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * (((co2_emission - 117) * 10) + (117 * 5)), 2)
                elif 151 <= co2_emission <= 200:
                    co2_tax = round_value(age_multiplier * (((co2_emission - 150) * 3.5) + (33 * 3)), 2)
                    reg_co2_fee = 46*5 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * (((co2_emission - 150) * 30) + (33 * 10) + (117 * 5)), 2)
                elif co2_emission >= 201:
                    co2_tax = round_value(age_multiplier * (((co2_emission - 200) * 4) + (50 * 3.5) + (33 * 3)), 2)
                    reg_co2_fee = 46*5 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * (((co2_emission - 200) * 50) + (50 * 30) + (33 * 10) + (117 * 5)), 2)
            else:
                co2_tax = 0
                reg_co2_fee = 0
            
            if general_engine_type == 'ICE' or general_engine_type == 'NOVC-HEV':
                if gross_weight > 2000:
                    weight_tax = round_value(age_multiplier * min((gross_weight - 2000) * 0.4, 400), 2)
                    reg_weight_fee = round_value(reg_fee_multiplier * min((gross_weight - 2000) * 2, 2000), 2)
                else:
                    weight_tax = 0
                    reg_weight_fee = 0
            elif general_engine_type == 'OVC-HEV':
                if gross_weight > 2200:
                    weight_tax = round_value(age_multiplier * min((gross_weight - 2200) * 0.4, 400), 2)
                    reg_weight_fee = round_value(reg_fee_multiplier * min((gross_weight - 2200) * 2, 2000), 2)
                else:
                    weight_tax = 0
                    reg_weight_fee = 0
            elif general_engine_type == 'ELECTRIC':
                if gross_weight > 2400:
                    weight_tax = round_value(age_multiplier * min((gross_weight - 2400) * 0.4, 440), 2)
                    reg_weight_fee = round_value(reg_fee_multiplier * min((gross_weight - 2400) * 2, 2200), 2)
                else:
                    weight_tax = 0
                    reg_weight_fee = 0
        
        elif (vehicle_type == 'N1_N1G' and ((max_net_power / kerb_mass) <= 0.20)) or (vehicle_type == 'M1_M1G' and is_house == 'Yes'):
            if general_engine_type != 'ELECTRIC':
                base_tax = 50
                reg_base_fee = 300
                
                if co2_emission < 205:
                    co2_tax = 0
                    reg_co2_fee = 69*2 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * (co2_emission * 2), 2)
                elif 205 <= co2_emission <= 250:
                    co2_tax = round_value(age_multiplier * ((co2_emission - 204) * 3), 2)
                    reg_co2_fee = 69*2 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * ((co2_emission - 204) * 30 + (204 * 2)), 2)
                elif 251 <= co2_emission <= 300:
                    co2_tax = round_value(age_multiplier * ((co2_emission - 250) * 3.5 + ((250 - 204) * 3)), 2)
                    reg_co2_fee = 69*2 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * ((co2_emission - 250) * 35 + ((250 - 204) * 30) + (204 * 2)), 2)
                elif co2_emission >= 301:
                    co2_tax = round_value(age_multiplier * ((co2_emission - 300) * 4 + ((300 - 250) * 3.5) + ((250 - 204) * 3)), 2)
                    reg_co2_fee = 69*2 if (general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available') else round_value(reg_fee_multiplier * ((co2_emission - 300) * 40 + ((300 - 250) * 35) + ((250 - 204) * 30) + (204 * 2)), 2)
                
                weight_tax = 0
                reg_weight_fee = 0
            else:  # ELECTRIC
                base_tax = 30
                co2_tax = 0
                weight_tax = 0
                reg_base_fee = 200
                reg_co2_fee = 0
                reg_weight_fee = 0
        
        # Calculate total tax
        if general_engine_type == 'OVC-HEV' and co2_standard == 'Not_available':
            total_tax = round_value(base_tax + weight_tax, 2)
        else:
            total_tax = round_value(base_tax + co2_tax + weight_tax, 2)
        
        # Calculate total registration fee
        total_reg_fee = round_value(reg_base_fee + reg_co2_fee + reg_weight_fee, 2)
        
        return {
            'base_tax': base_tax,
            'co2_tax': co2_tax,
            'weight_tax': weight_tax,
            'total_tax': total_tax,
            'reg_base_fee': reg_base_fee,
            'reg_co2_fee': reg_co2_fee,
            'reg_weight_fee': reg_weight_fee,
            'total_reg_fee': total_reg_fee
        }
    
    except Exception as e:
        print(f"Error calculating tax for vehicle {vehicle.get('MARK', '')}-{vehicle.get('MUDEL', '')}: {e}")
        return {
            'base_tax': 0,
            'co2_tax': 0,
            'weight_tax': 0,
            'total_tax': 0,
            'reg_base_fee': 0,
            'reg_co2_fee': 0,
            'reg_weight_fee': 0,
            'total_reg_fee': 0
        }

def main():
    input_file = "autod.csv"
    output_file = "autod_with_tax.csv"
    
    headers, vehicles = read_csv(input_file)
    
    if not vehicles:
        print("No data found. Exiting.")
        return
    
    # Calculate tax for each vehicle
    for vehicle in vehicles:
        tax_info = calculate_car_tax(vehicle)
        
        # Add tax information to the vehicle data
        vehicle['AASTAMAKS'] = str(tax_info['total_tax']).replace('.', ',')
        vehicle['REGISTREERIMISTASU'] = str(tax_info['total_reg_fee']).replace('.', ',')
    
    # Write results to new CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            # Add new headers for tax information
            new_headers = headers + ['AASTAMAKS', 'REGISTREERIMISTASU']
            
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_headers)
            
            for vehicle in vehicles:
                row = [vehicle.get(header, '') for header in headers]
                row.append(vehicle.get('AASTAMAKS', '0'))
                row.append(vehicle.get('REGISTREERIMISTASU', '0'))
                writer.writerow(row)
                
        print(f"Processing complete. Results written to {output_file}")
    
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    main()