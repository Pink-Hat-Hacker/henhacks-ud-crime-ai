# UD Crime AI - HenHacks 2024
##### /henhacks-ud-crime-ai

> Generative Machine Learning model trained on UD Police Daily Statistics from 2017-2021. When provided a LOCATION, DATE, & TIME it generates a prediction of what crime description may be committed.

## Try it yourself on Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Pink-Hat-Hacker/henhacks-ud-crime-ai/main)

## How
**Web scraping Data**
- First, the data needed to be gathered by the UD Police Statistics website. It was not easily available to download and was separated by day.
- A simple Python script got all the data into a CSV file.

**Cleaning Data**
- Although the data seemed usable it required some standardizing for an ML model.
1. The entries contained human error and typos so there was a lot of duplicate data with incorrect spelling or formatting. For example: `Trabant Student Center` & `Trabant Building`
2. The dates needed to be separated into DAY, MONTH, YEAR
3. The times needed to be standardized to military time and `:` removed

**Training the model**
- Using `sklearn` the model was trained on a DecisionTreeClassifier()
- The data was split into training and testing groups. The test size was 20% of the data.
- All the data was encoded so that they were numerical values because ML models are essentially mathematical models.
- The range of accuracy (since March 2024) is 20% - 30%

**Getting Predictions**
```
# Predict Crime Description for given Location and date/time
sample_location = "Smith Hall"
sample_time = 1200
sample_day = 3
sample_month = 5
sample_year = 2024

sample_location_encoded = label_encoders["Location"].transform([sample_location])[0]
predict_description = clf.predict([[sample_time, sample_location_encoded, sample_day, sample_month, sample_year]])

# Print the inverse encoding (readable text)
print(label_encoders["Description"].inverse_transform(predict_description))
```
Output: `['Trespass']`

## Resources
[UD Police Stats](https://www1.udel.edu/police/crime-stats/)

[Assembly AI Tutorials](https://www.youtube.com/playlist?list=PLcWfeUsAys2lpJzESyeRUVvJlU6ycjr-b)

[SKlearn](https://scikit-learn.org/stable/)
