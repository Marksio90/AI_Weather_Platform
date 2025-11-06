# 🌦 AI Weather Platform – DEMO

To jest **lekka wersja demo** zbudowana na bazie Twojej paczki.

## Co robi

- wyszukuje lokalizację przez `ingestion.open_meteo_client.search_locations`
- pobiera prognozę z `weather.services.fetch_weather_df`
- pokazuje temperaturę i opad w Streamlicie
- pozwala wybrać liczbę dni prognozy

## Jak uruchomić

1. Rozpakuj *oryginalną* paczkę (tę, którą mi wysłałeś) i w tym samym katalogu zapisz plik `demo_app.py` z tego archiwum.
2. Zainstaluj wymagania (takie jak w Twojej paczce), np.:

   ```bash
   pip install -r requirements.txt
   ```

3. Odpal demo:

   ```bash
   streamlit run demo_app.py
   ```

Jeśli moduły nie zostaną znalezione – upewnij się, że katalogi `ingestion/` oraz `weather/` znajdują się **obok** pliku `demo_app.py`.
