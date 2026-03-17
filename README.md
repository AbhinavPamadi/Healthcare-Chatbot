# Healthcare Chatbot (Rule-Based System)

## Overview
The **Healthcare Chatbot** is a **rule-based intelligent system** that helps users identify possible diseases based on their symptoms.

Unlike machine learning-based models, this chatbot uses **predefined rules and symptom-disease mappings** to make predictions. It evaluates user input, matches symptoms, and calculates severity to provide accurate and explainable results.

---

## Features
- Interactive chat interface using Streamlit  
- Rule-based decision system for disease prediction  
- Smart symptom matching (alias + fuzzy matching)  
- Severity-based scoring mechanism  
- Disease descriptions and precautions  
- Fast and deterministic responses (no training required)  

---

## Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Python  

### Libraries Used:
- pandas  
- csv  
- difflib  

### Core Approach:
- Rule-Based Expert System  
- Symptom-Disease Mapping  
- No Machine Learning model used  

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/AbhinavPamadi/Healthcare-Chatbot.git
cd Healthcare-Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run healthbot.py
```

---

## Working

The chatbot will ask you to:

1. Enter your name  
2. Enter symptoms one by one  
3. Type `done` when finished  
4. Enter the number of days you have had the symptoms  

The chatbot will then:

- Estimate symptom severity
- Predict possible diseases
- Show descriptions and precautions

---

## Example

```
Enter symptom: vomiting
Enter symptom: nausea
Enter symptom: headache
Enter symptom: done
From how many days: 2
```

Output:

```
Possible diseases:

Disease: Gastroenteritis
Match Score: 72%

Description: Infection that causes irritation and inflammation of the stomach and intestines.

Precautions:
- drink plenty of fluids
- avoid oily food
- rest
- consult doctor if symptoms worsen
```

---

## Dataset

The chatbot uses a symptom-disease dataset where:

- Columns represent symptoms
- Rows represent diseases
- `1` indicates presence of a symptom for that disease



## Disclaimer

This project is for educational purposes only and should not be used as a substitute for professional medical advice.
