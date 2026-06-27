from fastapi import FastAPI
import joblib
import uvicorn
from pydantic import BaseModel

mushroom_app = FastAPI()

model = joblib.load('model_mushroom.pkl')
scaler = joblib.load('scaler_mushroom.pkl')
mapping = joblib.load('1_0_mushroom.pkl')

class MushroomFeatures(BaseModel):
    cap_shape: str
    cap_surface: str
    cap_color: str
    bruises: str
    odor: str
    gill_attachment: str
    gill_spacing: str
    gill_size: str
    gill_color: str
    stalk_shape: str
    stalk_root: str
    ring_type: str
    spore_print_color: str
    population: str
    habitat: str


@mushroom_app.post('/predict')
async def predict_mushroom(mushroom: MushroomFeatures):
    features = [
        mapping['cap-shape'][mushroom.cap_shape],
        mapping['cap-surface'][mushroom.cap_surface],
        mapping['cap-color'][mushroom.cap_color],
        mapping['bruises'][mushroom.bruises],
        mapping['odor'][mushroom.odor],
        mapping['gill-attachment'][mushroom.gill_attachment],
        mapping['gill-spacing'][mushroom.gill_spacing],
        mapping['gill-size'][mushroom.gill_size],
        mapping['gill-color'][mushroom.gill_color],
        mapping['stalk-shape'][mushroom.stalk_shape],
        mapping['stalk-root'][mushroom.stalk_root],
        mapping['ring-type'][mushroom.ring_type],
        mapping['spore-print-color'][mushroom.spore_print_color],
        mapping['population'][mushroom.population],
        mapping['habitat'][mushroom.habitat],
    ]

    scaled = scaler.transform([features])
    prediction = model.predict(scaled)[0]
    probability = model.predict_proba(scaled)[0]

    return {
        'poisonous': bool(prediction == 0),
        'probability': round(float(max(probability)), 2)
    }


if __name__ == '__main__':
    uvicorn.run(mushroom_app, host='127.0.0.1', port=9000)