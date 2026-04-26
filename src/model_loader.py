import joblib

def load_model():
    return joblib.load("models/model.pkl")["model"]


#import mlflow.pyfunc

#def load_model():
#    return mlflow.pyfunc.load_model("models:/iris-model/latest")