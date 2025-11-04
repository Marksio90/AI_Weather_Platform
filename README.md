# AI-Driven Global Weather Forecast Platform

Paczka 7 dodaje:
- AI Model Slot – miejsce na podpięcie prawdziwego modelu (np. GraphCast, FourCastNet, własny downscaler),
- dwie przykładowe implementacje mock: `mock-graphcast` i `mock-downscaler`,
- slot jest wpięty PRZED postprocessingiem, więc cały pipeline działa bez zmian.

## Uruchomienie
```bash
pip install -r requirements.txt
streamlit run app.py
```
