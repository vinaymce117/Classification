import streamlit as st
import requests

st.title("🌸 Iris Classification App")
st.write("Enter flower measurements:")

# Sliders
f1 = st.slider("Sepal Length", 4.0, 8.0, 5.0)
f2 = st.slider("Sepal Width", 2.0, 4.5, 3.0)
f3 = st.slider("Petal Length", 1.0, 7.0, 4.0)
f4 = st.slider("Petal Width", 0.1, 2.5, 1.0)

if st.button("Predict"):
    payload = {
        "sepal_length": f1,
        "sepal_width": f2,
        "petal_length": f3,
        "petal_width": f4
    }

    try:
        with st.spinner("Predicting..."):
            response = requests.post(
                #"http://api:8000/predict", only for docker image local
                "http://iris-api.eastus.azurecontainer.io:8000/predict",
                json=payload,
                timeout=5
            )

        if response.status_code == 200:
            result = response.json()

            # ✅ Use label directly from API
            st.success(f"Prediction: {result['label']}")

        else:
            st.error(f"API error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to FastAPI. Make sure it is running.")

    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out.")

    except Exception as e:
        st.error(f"Unexpected error: {e}")