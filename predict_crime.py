# Assume `model` is the trained LSTM model and `label_encoders` contains the label encoders used during preprocessing

def predict_event(location, model, label_encoders):
    # Encode the location
    encoded_location = label_encoders['Location'].transform([location])
    
    # Create input data for prediction
    input_data = np.array([[0, 0, 0, encoded_location, 0]])  # Dummy values for time, date occurred, description, and disposition
    
    # Make prediction
    predicted_incident_number = model.predict(input_data)
    
    # Decode predicted values
    decoded_location = label_encoders['Location'].inverse_transform(encoded_location)
    
    return {
        'Location': decoded_location,
        'Incident #': predicted_incident_number,
        # You can also predict other features like time, date, and description similarly
    }

# Example usage
predicted_event = predict_event('Some Location', model, label_encoders)
print(predicted_event)
