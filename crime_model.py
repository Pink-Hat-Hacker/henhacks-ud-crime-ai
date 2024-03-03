import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Step 1: Data Preparation
def preprocess_data(csv_file):
    data = pd.read_csv(csv_file)
    
    # Drop rows with missing values
    data.dropna(inplace=True)
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['Description', 'Location', 'Disposition']
    for col in categorical_columns:
        label_encoders[col] = LabelEncoder()
        data[col] = label_encoders[col].fit_transform(data[col])
    
    # Split data into features and targets
    X = data[['Time', 'Date Occurred', 'Description', 'Location', 'Disposition']].values
    y = data[['Incident #']].values
    
    return X, y, label_encoders

# Load and preprocess the data
csv_file = "clean_crime_data.csv"
X, y, label_encoders = preprocess_data(csv_file)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Model Selection and Architecture
model = Sequential([
    LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dense(1)  # Output a single value (Incident #)
])

# Step 3: Compile the model
model.compile(optimizer='adam', loss='mse')

# Step 4: Training Loop
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Step 8: Saving the Model
model.save("event_prediction_model.h5")
