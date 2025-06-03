
import streamlit as st
import pandas as pd
import requests
import uuid
from datetime import datetime

# --- Session ID ---
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

# --- Data setup ---
data = [
    ["Rosslyn Coffee", "EC4N", "Medium", "Bold, chocolatey, toffee, nutty, sweet"],
    ["Notes Coffee", "EC4M", "Medium", "Chocolatey, nutty, citrusy, caramel, sweet"],
    ["Black Sheep Coffee", "EC3V", "Medium", "Chocolatey, nutty, full-bodied, bold, low-acidity"],
    ["WatchHouse", "EC2M", "Medium", "Chocolatey, nutty, fruity, creamy, sweet"],
    ["Grind", "EC3V", "Medium", "Chocolatey, nutty, fruity, caramel, sweet"],
    ["Saint Espresso", "EC2V", "Medium", "Chocolatey, nutty, caramel, full-bodied, rich"],
    ["Alchemy Coffee", "EC2M", "Medium", "Chocolatey, nutty, fruity, creamy, balanced"]
]

df = pd.DataFrame(data, columns=["Name", "Postcode", "Roast Level", "Flavour Profile"])

# --- App interface ---
st.title("Bean Thinking")
st.subheader("Find the perfect coffee based on your taste")

nickname = st.text_input("Optional: enter a nickname or short ID (for feedback tracking)")

# Question 1: Flavour Preferences
flavour_options = ["Chocolatey", "Nutty", "Fruity", "Sweet", "Bold", "Smooth", "Floral", "Citrus", "Spicy", "Earthy"]
flavour_choices = st.multiselect("What flavours do you enjoy in coffee? (Pick up to 3)", flavour_options, max_selections=3)

# Question 2: Coffee Style
style = st.radio("How do you usually drink your coffee?", ["Milk-based", "Black", "Filter / Hand-brewed"])

# Question 3: Taste Adventure Level
adventure = st.radio("How adventurous are your taste buds?", ["Classic", "Balanced", "Adventurous"])

# Question 4: Postcode
postcode = st.text_input("Enter your postcode (e.g. EC4R 3TL)")

# --- Matching Logic ---
def match_flavours(user_choices, profile):
    profile_words = [w.strip().lower() for w in profile.split(",")]
    matches = set(w.lower() for w in user_choices) & set(profile_words)
    return len(matches)

if st.button("Find My Coffee Matches"):
    if not flavour_choices or not postcode:
        st.warning("Please complete all questions including postcode.")
    else:
        df["Match Score"] = df["Flavour Profile"].apply(lambda x: match_flavours(flavour_choices, x))
        sorted_df = df.sort_values(by="Match Score", ascending=False)

        st.success("Here are your top matches:")
        top_matches = []
        for i, row in sorted_df.head(3).iterrows():
            st.markdown(f"**{row['Name']}** ({row['Postcode']})")
            st.markdown(f"Roast: {row['Roast Level']}")
            st.markdown(f"Flavour Profile: *{row['Flavour Profile']}*")
            st.markdown("---")
            top_matches.append(row['Name'])

        st.subheader("☕ Feedback")
        feedback_rating = st.radio("How well did this match your taste?", ["Perfect match", "Pretty good", "Not really", "Didn't try any"])
        feedback_comments = st.text_area("Tell us more (optional):")

        if st.button("Submit Feedback"):
            form_url = "https://docs.google.com/forms/d/e/FORM_ID/formResponse"
            form_data = {
                "entry.FORM_FIELD_ID_1": nickname,
                "entry.FORM_FIELD_ID_2": st.session_state['session_id'],
                "entry.FORM_FIELD_ID_3": datetime.now().isoformat(),
                "entry.FORM_FIELD_ID_4": ", ".join(flavour_choices),
                "entry.FORM_FIELD_ID_5": style,
                "entry.FORM_FIELD_ID_6": adventure,
                "entry.FORM_FIELD_ID_7": postcode,
                "entry.FORM_FIELD_ID_8": ", ".join(top_matches),
                "entry.FORM_FIELD_ID_9": feedback_rating,
                "entry.FORM_FIELD_ID_10": feedback_comments
            }
            try:
                requests.post(form_url, data=form_data)
                st.success("Thanks for your feedback!")
            except:
                st.error("Failed to submit feedback. Try again later.")
