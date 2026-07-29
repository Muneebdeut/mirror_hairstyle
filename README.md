# AI Hairstyle Advisor

An end-to-end, production-ready AI web application that enables users to upload a photo, analyze their facial landmark geometry and estimate face shape, choose style presentation preferences, discover personalized top-ranked hairstyles, and preview chosen styles using an AI Virtual Try-On before/after slider.

---

## 🌟 Key Features

- **Computer Vision Face Mesh Landmark Analysis**: Extracts 468 3D facial landmarks using MediaPipe to compute face length, width, forehead width, cheekbone width, jaw width, and aspect ratios.
- **Face Shape Estimation**: Interpretable rule-based classifier estimating `Oval`, `Round`, `Square`, `Heart`, and `Oblong` shapes with confidence scores and disclaimers.
- **Inclusive Hairstyle Preference Filtering**: Filter style recommendations by `Masculine`, `Feminine`, `Unisex`, or `No Preference` (Default: `No Preference`). Treat preferences as styling filters rather than gender classification.
- **Weighted Recommendation Engine**: Ranks hairstyles based on Face Shape Compatibility (45%), Hairstyle Preference (25%), Hair Characteristics (15%), and Maintenance (15%), complete with custom suitability explanations.
- **AI Virtual Try-On Engine**: Abstracted provider system supporting OpenAI Vision/Editing API or a high-quality local fallback renderer when API keys are absent.
- **Interactive Before/After Slider**: Real-time draggable visual slider comparing original user portrait with AI-generated virtual hairstyle preview.
- **Privacy First**: Images are processed temporarily in memory with no permanent storage by default.

---

## 🏗️ Architecture & Project Structure

```text
ai-hairstyle-advisor/
│
├── frontend/                     # Next.js 14 App Router, TypeScript, Tailwind CSS
│   ├── app/                      # Page routes & root layout
│   ├── components/               # ImageUploader, FaceAnalysis, BeforeAfterSlider, etc.
│   ├── lib/                      # API client & helpers
│   ├── types/                    # TypeScript interfaces
│   ├── Dockerfile
│   └── package.json
│
├── backend/                      # Python FastAPI, OpenCV, MediaPipe, Pydantic
│   ├── app/
│   │   ├── main.py               # FastAPI application entrypoint & CORS config
│   │   ├── api/                  # Routes for face analysis, recommendations, try-on
│   │   ├── ml/                   # Face shape classifier, catalog, recommender engine
│   │   ├── services/             # Face mesh analysis, hair analysis, virtual try-on
│   │   ├── models/               # Pydantic schemas & data models
│   │   └── utils/                # Image encoding & decoding utilities
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── training/                     # ML Training pipeline roadmap
│   ├── prepare_dataset.py        # Dataset CSV preparation script
│   ├── train_face_shape_model.py # MLP model training script
│   ├── train_recommendation_model.py # Collaborative filtering model script
│   └── evaluate_model.py         # Precision, Recall & NDCG@5 metrics
│
├── tests/                        # Pytest suite
│   ├── test_face_analysis.py
│   ├── test_face_shape.py
│   ├── test_recommendations.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn
- **Computer Vision**: MediaPipe Face Mesh, OpenCV
- **AI Virtual Try-On**: Abstracted OpenAI DALL-E / Vision API provider + Local fallback renderer
- **Testing**: Pytest, FastAPI TestClient
- **DevOps**: Docker, Docker Compose

---

## 🚀 Installation & Local Running

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm / yarn

### 1. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Running the Backend API

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs will be live at: `http://localhost:8000/docs`

### 3. Running the Frontend Application

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at: `http://localhost:3000`

---

## 🧪 Running Unit Tests

Run the backend pytest test suite to verify face detection, face shape classification, recommendation ranking, and API validation:

```bash
# From the root directory or inside backend environment:
pytest tests/
```

All unit tests check:
1. `test_face_analysis.py`: Edge cases when no face is detected or synthetic landmark arrays are passed.
2. `test_face_shape.py`: Classification logic verifying Oval, Round, and Square ratio thresholds.
3. `test_recommendations.py`: Weighted match scores, preference ranking, and top 5 selection.
4. `test_api.py`: FastAPI endpoint health, payload schemas, and virtual try-on mock responses.

---

## 🐳 Docker Deployment

To launch the full multi-container application stack with Docker Compose:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

---

## 🤖 Machine Learning Roadmap

The MVP currently uses MediaPipe Face Mesh + rule-based geometric ratios for face shape estimation and configurable weighted ranking for recommendations. The code is structured for direct drop-in replacement with trained ML models:

1. **Synthetic & Real Dataset Schema** (`training/prepare_dataset.py`)
   - Prepares landmark vectors, hair traits, and user feedback ratings.
2. **Deep Neural Network Classifier** (`training/train_face_shape_model.py`)
   - Multi-layer Perceptron (MLP) for landmark-to-shape classification.
3. **Neural Collaborative Filtering** (`training/train_recommendation_model.py`)
   - Learns $P(\text{hairstyle suitability} \mid \text{face shape}, \text{hair traits}, \text{user preference})$.

---

## 🔒 Privacy & Safety

- Images uploaded to the API are processed in-memory.
- Temporary files are immediately cleaned up.
- API keys are secured server-side and never exposed to client browsers.
- No user gender is classified or inferred from facial photos.
