import streamlit as st
import pandas as pd
import csv
import difflib

# Load Training Data

training = pd.read_csv("Data/Training.csv")
symptoms = [s.strip().lower() for s in training.columns[:-1]]

disease_rules = {}

for _, row in training.iterrows():
    disease = row["prognosis"]

    sym_list = [symptoms[i] for i in range(len(symptoms)) if row.iloc[i] == 1]

    if disease not in disease_rules:
        disease_rules[disease] = set()

    disease_rules[disease].update(sym_list)

for d in disease_rules:
    disease_rules[d] = list(disease_rules[d])

# Dictionaries

severityDictionary = {}
description_list = {}
precautionDictionary = {}


# Symptom alias mapping

symptom_alias = {
    "cold": ["runny_nose", "continuous_sneezing", "chills"],
    "fever": ["high_fever"],
    "cough": ["cough"],
    "headache": ["headache"],
    "vomiting": ["vomiting"],
    "stomach pain": ["abdominal_pain"],
    "sore throat": ["throat_irritation"]
}


# Load CSV metadata

def load_severity():
    with open("MasterData/symptom_severity.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            severityDictionary[row[0]] = int(row[1])


def load_description():
    with open("MasterData/symptom_Description.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            description_list[row[0]] = row[1]


def load_precautions():
    with open("MasterData/symptom_precaution.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]


# Symptom suggestion

def suggest_symptoms(word):

    word = word.strip().lower().replace(" ", "_")
    matches = [s for s in symptoms if word in s or s in word]
    if matches:
        return matches
    matches = difflib.get_close_matches(word, symptoms, n=5, cutoff=0.2)
    return matches


def match_symptom(user_input):
    user_input = user_input.lower().strip()
    if user_input in symptom_alias:
        return symptom_alias[user_input]
    user_input = user_input.replace(" ", "_")
    matches = suggest_symptoms(user_input)
    return matches


# Rule scoring

def disease_score(user_symptoms):
    scores = {}
    for disease, rule_symptoms in disease_rules.items():
        matched = list(set(user_symptoms) & set(rule_symptoms))
        if len(matched) < 2:
            continue
        matched_severity = sum(severityDictionary.get(s, 1) for s in matched)
        max_severity = sum(severityDictionary.get(s, 1) for s in rule_symptoms)

        score = matched_severity / max_severity
        scores[disease] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# Severity check

def check_severity(user_symptoms, days):
    total = 0

    for s in user_symptoms:
        total += severityDictionary.get(s, 0)

    score = (total * days) / (len(user_symptoms) + 1)

    if score > 15:
        return "consult"
    else:
        return "mild"


# Load metadata

load_severity()
load_description()
load_precautions()


# Streamlit Chat UI

st.title("Healthcare Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.symptoms = []
    st.session_state.step = 0
    st.session_state.days = 0
    st.session_state.pending_symptoms = []


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# User input
user_input = st.chat_input("What is your name?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Step 0 - ask name
    if st.session_state.step == 0:
        response = f"Hello {user_input}. Please tell me one symptom."
        st.session_state.step = 1

    # Step 1 - collect symptoms
    elif st.session_state.step == 1:

        if len(st.session_state.pending_symptoms) > 0:

            try:
                choice = int(user_input)
                symptom = st.session_state.pending_symptoms[choice]

                st.session_state.symptoms.append(symptom)
                st.session_state.pending_symptoms = []

                response = f"Added {symptom}. Enter another symptom or type 'done'."
            except:
                response = "Please enter a valid number."
        else:
            if user_input.lower() == "done":
                response = "From how many days are you experiencing these symptoms?"
                st.session_state.step = 2
            else:
                matches = match_symptom(user_input)

                if len(matches) == 0:
                    response = "Symptom not found. Please try another."
                elif len(matches) == 1:
                    symptom = matches[0]
                    st.session_state.symptoms.append(symptom)

                    response = f"Added {symptom}. Enter another symptom or type 'done'."
                else:
                    st.session_state.pending_symptoms = matches

                    options = "\n".join(
                        [f"{i}. {m}" for i, m in enumerate(matches)]
                    )

                    response = f"Did you mean:\n\n{options}\n\nType the number."

    # Step 2 - get days
    elif st.session_state.step == 2:
        st.session_state.days = int(user_input)
        severity = check_severity(st.session_state.symptoms, st.session_state.days)
        ranked = disease_score(st.session_state.symptoms)
        result = ""

        if severity == "consult":
            result += "You should consult a doctor.\n\n"
        else:
            result += "Symptoms appear mild but take precautions.\n\n"

        result += "Possible diseases:\n\n"

        for disease, score in ranked[:3]:
            result += f"**{disease}** ({round(score*100,2)}%)\n"

            if disease in description_list:
                result += description_list[disease] + "\n"

            if disease in precautionDictionary:
                result += "\n\nPrecautions:\n"
                for p in precautionDictionary[disease]:
                    result += "- " + p + "\n"

            result += "\n"

        response = result
        st.session_state.step = 3


    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)