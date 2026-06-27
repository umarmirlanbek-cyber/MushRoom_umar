from fastapi import FastAPI
import joblib
import uvicorn
from pydantic import BaseModel

mushroom_app = FastAPI()

model = joblib.load('model_mushroom.pkl')
scaler = joblib.load('scaler_mushroom.pkl')

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
        0 if mushroom.cap_shape == 'x' else 1 if mushroom.cap_shape == 'b' else 2 if mushroom.cap_shape == 's' else 3 if mushroom.cap_shape == 'f' else 4 if mushroom.cap_shape == 'k' else 5,
        0 if mushroom.cap_surface == 's' else 1 if mushroom.cap_surface == 'y' else 2 if mushroom.cap_surface == 'f' else 3,
        0 if mushroom.cap_color == 'n' else 1 if mushroom.cap_color == 'y' else 2 if mushroom.cap_color == 'w' else 3 if mushroom.cap_color == 'g' else 4 if mushroom.cap_color == 'e' else 5 if mushroom.cap_color == 'p' else 6 if mushroom.cap_color == 'b' else 7 if mushroom.cap_color == 'u' else 8 if mushroom.cap_color == 'c' else 9,
        0 if mushroom.bruises == 't' else 1,
        0 if mushroom.odor == 'p' else 1 if mushroom.odor == 'a' else 2 if mushroom.odor == 'l' else 3 if mushroom.odor == 'n' else 4 if mushroom.odor == 'f' else 5 if mushroom.odor == 'c' else 6 if mushroom.odor == 'y' else 7 if mushroom.odor == 's' else 8,
        0 if mushroom.gill_attachment == 'f' else 1,
        0 if mushroom.gill_spacing == 'c' else 1,
        0 if mushroom.gill_size == 'n' else 1,
        0 if mushroom.gill_color == 'k' else 1 if mushroom.gill_color == 'n' else 2 if mushroom.gill_color == 'g' else 3 if mushroom.gill_color == 'p' else 4 if mushroom.gill_color == 'w' else 5 if mushroom.gill_color == 'h' else 6 if mushroom.gill_color == 'u' else 7 if mushroom.gill_color == 'e' else 8 if mushroom.gill_color == 'b' else 9 if mushroom.gill_color == 'r' else 10 if mushroom.gill_color == 'y' else 11,
        0 if mushroom.stalk_shape == 'e' else 1,
        0 if mushroom.stalk_root == 'e' else 1 if mushroom.stalk_root == 'c' else 2 if mushroom.stalk_root == 'b' else 3 if mushroom.stalk_root == 'r' else 4,
        0 if mushroom.ring_type == 'p' else 1 if mushroom.ring_type == 'e' else 2 if mushroom.ring_type == 'l' else 3 if mushroom.ring_type == 'f' else 4,
        0 if mushroom.spore_print_color == 'k' else 1 if mushroom.spore_print_color == 'n' else 2 if mushroom.spore_print_color == 'u' else 3 if mushroom.spore_print_color == 'h' else 4 if mushroom.spore_print_color == 'w' else 5 if mushroom.spore_print_color == 'r' else 6 if mushroom.spore_print_color == 'o' else 7 if mushroom.spore_print_color == 'y' else 8,
        0 if mushroom.population == 's' else 1 if mushroom.population == 'n' else 2 if mushroom.population == 'a' else 3 if mushroom.population == 'v' else 4 if mushroom.population == 'y' else 5,
        0 if mushroom.habitat == 'u' else 1 if mushroom.habitat == 'g' else 2 if mushroom.habitat == 'm' else 3 if mushroom.habitat == 'd' else 4 if mushroom.habitat == 'p' else 5 if mushroom.habitat == 'w' else 6,
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