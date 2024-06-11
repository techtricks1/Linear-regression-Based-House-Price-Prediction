from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load your trained model and feature names
model = joblib.load('./linear_regression_model.pkl')
feature_names = joblib.load('feature_names.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print(f"Received input data: {data}")

        # Convert categorical data to match the model's expectations
        categorical_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
        for col in categorical_columns:
            if col in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']:
                data[col] = int(data[col])
            elif col == 'furnishingstatus':
                # Encode 'furnishingstatus' as dummies (one-hot encoding)
                if data[col] == 'Fully Furnished':
                    data.update({'furnishingstatus_Fully Furnished': 1, 'furnishingstatus_Semi-Furnished': 0, 'furnishingstatus_Unfurnished': 0})
                elif data[col] == 'Semi-Furnished':
                    data.update({'furnishingstatus_Fully Furnished': 0, 'furnishingstatus_Semi-Furnished': 1, 'furnishingstatus_Unfurnished': 0})
                elif data[col] == 'Unfurnished':
                    data.update({'furnishingstatus_Fully Furnished': 0, 'furnishingstatus_Semi-Furnished': 0, 'furnishingstatus_Unfurnished': 1})
                data.pop('furnishingstatus', None)

        print(f"Transformed input data: {data}")

        # Convert form data to DataFrame
        input_data = pd.DataFrame([data])

        # Add missing features with default value 0 and ensure correct order
        for feature in feature_names:
            if feature not in input_data.columns:
                input_data[feature] = 0
        
        input_data = input_data[feature_names]

        print(f"Final input data for prediction: {input_data}")

        # Make predictions
        prediction = model.predict(input_data)

        return jsonify({'predicted_price': prediction[0]})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
