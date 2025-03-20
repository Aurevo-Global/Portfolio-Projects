import json
import pickle
import numpy as np

import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")

# Initialize variables
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1 

    return round(__model.predict([x])[0],2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts... start")
    global __data_columns, __locations, __model

    try:
        # Load data columns from JSON file
        with open(".\\server\\artifacts\\columns.json", 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # Assuming locations start from the 4th column

        # Load the model from pickle file
        global __model
        with open(".\\server\\artifacts\\bengaluru_home_prices_model.pickle", 'rb') as f:
            __model = pickle.load(f)

        print("Loading saved artifacts... done")
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the artifact files are in the correct location.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))