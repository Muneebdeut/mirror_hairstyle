# AI Hairstyle Advisor - Backend API

FastAPI backend service powering computer vision facial landmark detection, face shape estimation, personalized hairstyle recommendation ranking, and AI virtual try-on previews.

## Features

- **MediaPipe Face Mesh Integration**: 468 facial landmark extraction for precise 3D face geometric measurements.
- **Rule-Based & Extensible ML Face Shape Classifier**: Classifies face shapes into Oval, Round, Square, Heart, and Oblong with confidence metrics.
- **Gender-Neutral Preference Ranking**: Allows style exploration filters (`masculine`, `feminine`, `unisex`, `no_preference`) without classifying user gender.
- **Hairstyle Catalog & Recommender Engine**: Weighted score ranking engine based on face shape fit (45%), style preference (25%), hair texture/length (15%), and maintenance (15%).
- **Abstracted AI Virtual Try-On Provider**: Supports OpenAI Vision/Editing API or built-in photorealistic local image overlay fallback when API keys are absent.

## Installation

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

## Running the Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation available at: `http://localhost:8000/docs`

## Environment Variables

Create `.env` file in root or backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```
