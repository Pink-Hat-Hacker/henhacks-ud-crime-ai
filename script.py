# %% [markdown]
# # 2024 HENHACKS - AI Predictive UD Crime Model
# 
# *This Machine Learning AI model uses cleaned data from UD Police Daily Statistics (2017-2021) and creates crome description predictions based on an inputed LOCATION, DATE, & TIME.*

# %% [markdown]
# ### Step 1: Clean and Check Data
# 
# Most of the data was cleaned in excel by:
# - splitting the dates to day, month year
# - reducing the errors so that Locations, and Crime Descriptions aren't duplicated
# - standardizing time data

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# removes warnings
pd.options.mode.chained_assignment = None

# %%
pd.set_option('display.max_columns', None)
crimes = pd.read_csv('clean_crime_data.csv')
crimes

# %%
''' GRAPHING CRIME LOCATIONS '''
location_counts = crimes['Location'].value_counts()

# Extract location names and corresponding counts
locations = location_counts.index.tolist()
counts = location_counts.values.tolist()

# Plotting the pie chart
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=locations)
plt.title('Location Occurrence')
plt.show()

# %%
''' GRAPHING CRIME DESCRIPTION '''

description_count = crimes['Description'].value_counts()

# Extract description names and corresponding counts
description = description_count.index.tolist()
counts = description_count.values.tolist()

# Plotting the pie chart
plt.figure(figsize=(10, 8))
plt.pie(counts, labels=description)
plt.title('Crime Type Occurrence')
plt.show()

# %% [markdown]
# ### Step 2: Data Preparation
# 
# Machine learning models are essentially mathematical models. So it requires numerial values.

# %%
from sklearn.preprocessing import LabelEncoder

# Remove columns that are not needed and create dataset
crimes = crimes[['Time', 'Description', 'Location', 'Day Occurred', 'Month Occurred', 'Year Occurred']]

# Encode categorical values
label_encoders = {}
for col in crimes:
    label_encoders[col] = LabelEncoder()
    crimes[col] = label_encoders[col].fit_transform(crimes[col])

# Split into X and Y (target and feature categories)
X_crimes = crimes[['Time', 'Location', 'Day Occurred', 'Month Occurred', 'Year Occurred']]
y_crimes = crimes[['Description']]

# Make categorical values numerical
X_crimes = pd.get_dummies(X_crimes)

# %% [markdown]
# ### Step 3: Implement Model Type

# %%
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_crimes, y_crimes, test_size=0.2, random_state=42)

# Define preprocessing and training
clf = DecisionTreeClassifier().fit(X_train.values, y_train.values)

y_pred = clf.predict(X_test.values)
y_pred

# %% [markdown]
# #### Accuracy

# %%
# Returns the coefficient of determination of the prediction
# Basically how well it did ... not great
clf.score(X_test.values, y_test.values)

# %% [markdown]
# ### Step 4: Evaluate Model
# 
# Attempting to understand what all this data means :3

# %%
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
cm

# %%
import seaborn as sns

plt.figure(figsize=(20,20))
sns.heatmap(cm, annot=True, fmt='g', xticklabels=clf.classes_, yticklabels=clf.classes_)

# %% [markdown]
# ## Example Prediction

# %%
# Predict Crime Description for given Location and date/time
sample_location = "Smith Hall"
sample_time = 1200
sample_day = 3
sample_month = 5
sample_year = 2024

sample_location_encoded = label_encoders["Location"].transform([sample_location])[0]

predict_description = clf.predict([[sample_time, sample_location_encoded, sample_day, sample_month, sample_year]])
print(label_encoders["Description"].inverse_transform(predict_description))


