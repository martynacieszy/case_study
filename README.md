# Praca dyplomowa: "Analiza rynku nieruchomości w Nowym Jorku pod kątem inwestycji na wynajem."

Opis tej analizy można znaleźć w DyplomMartynaCieszynska22524.ptpx.
Dane źródłowe dla zadania zostały zapisane w folderze "dane_zrodlowe": Airbnb_data_New_York.csv, Property_sales_data_New_York.csv.

Analiza została podzielona na dwa główne skrypty:
1. 1_PrzygotowanieDanych.ipynb
2. 2_AplikacjaStreamlit.py

W pierwszym skrypcie dane źródłowe zostały odczytane, przekształcone do ramki danych i zmanipulowane w celu uzyskania najlepszej jakości danych. Zostało to przeprowadzone przy użyciu Jupyter Notebook.
Dane wyjściowe z tej procedury są przechowywane w folderze "dane_przeksztalcone" jako sales_NY.json i airbnb_NY.json.
Na podstawie dwóch wspomnianych plików .json uruchomiono 2_AplikacjaStreamlit.py w Streamlit Community Cloud z GitHub. W aplikacji wykorzystano funkcje z pliku funkcje_pomocnicze.py z folderu pliki_pomocnicze. 
Stworzona aplikacja Streamlit znajduje się pod adresem:
https://dyplom-martyna-cieszynska.streamlit.app/

W celu zobaczenia wyników wystarczy wejść w powyższy link.

Aby uruchomić aplikację lokalnie należy zainstalować biblioteki z pliku requirements.txt. Plik ten oraz mapbox_token z folderu pliki_pomocnicze, jest niezbędny w repozytorium do uruchomienia aplikacji webowej.