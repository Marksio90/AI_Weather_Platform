# AI-Driven Global Weather Forecast Platform

Ten projekt to modularna, AI-first aplikacja pogodowa oparta o Streamlit + zestaw usług Python.

**W tej paczce (7) dochodzi kluczowy element: _AI Model Slot_.**

Dzięki temu możesz:
- w jednym miejscu podpiąć _prawdziwy_ model pogodowy ML (np. GraphCast, FourCastNet, Pangu-Weather, własny serwis downscalingu),
- testować różne warianty modeli bez zmiany reszty aplikacji,
- wciąż korzystać z istniejącego AI postprocessingu, alertów, TTS i walidacji.

---

## Co jest w paczce 7

- ✅ **AI Model Slot** – pojedynczy punkt wejścia w kodzie (`ai/model_slot.py`), w którym wybierasz, jakiego modelu chcesz użyć.
- ✅ **Dwie przykładowe implementacje mock**:
  - `mock-graphcast` – udaje poprawę opadów i lekkie wygładzenie temperatury,
  - `mock-downscaler` – udaje lokalny downscaling zależny od szerokości geograficznej.
- ✅ Slot jest wpięty **PRZED** modułem AI postprocessingu → najpierw model, potem nasze korekty.
- ✅ Front w Streamlicie dostał selektor „AI Model slot”, więc możesz klikać warianty z UI.
- ✅ Reszta pipeline’u (prognoza → AI → alerty → tekst → TTS → walidacja) działa bez zmian.

---

## Struktura (skrót)

- `app.py` – główny Streamlit, UI, sidebar, routing modułów
- `core/` – config, i18n, auth, storage
- `ingestion/` – pobieranie danych (Open-Meteo, geocoding)
- `weather/` – normalizacja do `DataFrame`
- `ai/` – postprocessing, tekst prognozy, TTS, **model slot**
- `ui/` – layout, alerty, radar, sekcje, walidacja

---

## Jak to działa (pipeline)

1. Użytkownik wybiera lokalizację (geocoding Open-Meteo albo ręcznie lat/lon).
2. Aplikacja pobiera prognozę godzina po godzinie z wybranego źródła (aktualnie: `open-meteo`).
3. Dane trafiają do **AI Model Slot** – tu możesz podmienić na swój model ML.
4. Potem leci **AI postprocessing** (wygładzanie, przycinanie ekstremów).
5. Na podstawie przetworzonych danych generowane są:
   - wykresy,
   - alerty pogodowe,
   - tekst prognozy (PL/EN),
   - opcjonalnie TTS (gTTS).
6. Jeśli włączony jest tryb developer / enterprise – można wgrać własne obserwacje i zrobić walidację.

---

## Uruchomienie (lokalnie)

```bash
pip install -r requirements.txt
streamlit run app.py
