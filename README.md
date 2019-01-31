# O projekcie

Projekt miał na celu badanie wpływu długości komórki w automatach komórkowych symulujących ruch drogowy.

Wyniki naszych badań są zebrany w pliku `Projekt Zespołowy - 2019.pdf`

## Zaimplementowane modele

Model | Ścieżka | Autor
------|---------|----------
BML   | `src/BML/` | Jakub Rutkowski
Chowdhury | `src/Chowdhury/` | Bartosz Wilczański
Nagel | `src/nagel_sch_m.py` | Karol Działowski
Rickert Asymetryczny | `src/ricker_asym.py` | Karol Działowski
Rickert Symetryczny | `src/rickert_sym.py` | Karol Działowski
Knospe | `src/knospe.realistic.py` | Karol Działowski
BHJ | `src/BHJ.pu` | Jakub Rutkowski

### Dodatkowe pliki

Plik | Opis
-----| --------
`src/comprasion.py` | Skrypt do porównywania modeli - generuje diagramy
`src/data_presentation.py` | Skrypt z metodami do generowania diagramów fundamentalnych i wizualizacji
`src/generate_diagrams_for_document.py` | Skrypt do generowania diagramów na podstawie zewnętrznych danych
`src/nagel_sch.py` | Model Nagela podstawowy - bez zmiennej długości komórki
`src/tests/` | Testy jednostkowe dla modelu Knospe


