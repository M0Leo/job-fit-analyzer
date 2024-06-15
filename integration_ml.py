# -*- coding: utf-8 -*-
"""integration-ML

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Ajnl8gFOXDIsoIpPhmUjiEsG0xu4VZ2
"""

from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd

app = Flask("Content_Based_System")

model_title = RandomForestClassifier(random_state=40)
model_location = RandomForestClassifier(random_state=42)
tfidf = TfidfVectorizer()

file_path = 'jobss.csv'
jobs_data = pd.read_csv(file_path)
jobs_data.dropna(subset=['Job Title'], inplace=True)

X = tfidf.fit_transform(jobs_data['Key Skills'].astype(str))

y_title = jobs_data['Job Title']
model_title.fit(X, y_title)

y_location = jobs_data['Location']
model_location.fit(X, y_location)

@app.route('/predict', methods=['GET'])
def predict_job_title_and_location():
    data = request.get_json()
    skills = data['skills']
    top_n = data.get('top_n', 5)
    relevance_threshold = data.get('relevance_threshold', 0.08)

    skills_transformed = tfidf.transform([skills.lower()])

    probs_title = model_title.predict_proba(skills_transformed)[0]
    top_n_indices_title = np.argsort(probs_title)[-top_n:]
    top_n_probs_title = probs_title[top_n_indices_title]
    relevant_titles = [model_title.classes_[i] for i, prob in zip(top_n_indices_title, top_n_probs_title) if prob >= relevance_threshold]

    predicted_title = np.random.choice(relevant_titles) if relevant_titles else 'No relevant title found'

    probs_location = model_location.predict_proba(skills_transformed)[0]
    top_n_indices_location = np.argsort(probs_location)[-top_n:]
    predicted_location = np.random.choice([model_location.classes_[i] for i in top_n_indices_location])

    return jsonify({
        'predicted_title': predicted_title,
        'predicted_location': predicted_location
    })

if __name__ == '__main__':
    app.run(debug=True)
