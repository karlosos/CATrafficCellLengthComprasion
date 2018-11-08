/**
  Model NagSch zaimplementowany przez Bartka.

  W tym modelu przyjmujemy, ze kazdy pojazd ma wlasna predkosc
  maksymalna, do ktorej moze sie rozpedzic.

  W odroznieniu od standardowego modelu, konce drogi nie sa polaczone,
  czyli droga nie jest cykliczna.

  Bartek generuje pojazdy na poczatku drogi i usuwa je, jezeli
  wyjechaly poza trase.

  Brak rowniez fazy losowego zwalniania. Pojazdy samoistnie nie zwalniaja
  z przyczyn losowych.
*/

#include <stdio.h>
#include <iostream>
#include <time.h>
#include <chrono>
#include <thread>

using namespace std;
// dlugosc drogi
static int W = 100;

class pojazd
{
public:
    int V;
	int Vmax;
	//	int wielkosc;
	pojazd()
	{
        // losowanie predkosci i predkosci maksymalnej
		Vmax = rand() % 3 + 1;
		this->V = rand() % Vmax + 1;
	}

    void wyswietl() {
        cout << V;
    }

	void speedup() {
		if (V < Vmax) {
			V++;
		}
	}
};

void generator(pojazd ***&d, pojazd *&p)
{
    // geberuje pojazdy tylko dla dolnej linii
	p = new pojazd;
	d[1][0] = p;
}

void wyswietlanie(pojazd ***&d) {
    // wyswietlanie dwoch wektorow
	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < W; j++) {
            if (d[i][j] == nullptr)
			{
				cout << '-';
			}
			else {
				d[i][j]->wyswietl();
			}
		}
		cout << endl;
	}

}

void odswiezanie(pojazd ***&d)
{
	pojazd *t;
	pojazd ***r = new pojazd **[2];

    r[0] = new pojazd*[static_cast<unsigned long int>(W)];
    r[1] = new pojazd*[static_cast<unsigned long int>(W)];
    // zerowanie pomocniczych tablic
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < W; j++) {
            r[i][j] = nullptr;
        }
    }

	int x, y;
	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < W; j++)
		{
			t = d[i][j];
            // jezeli w komorce jest pojazd
            if (t != nullptr)
			{
                // wylicza nastepna przewidywana pozycje pojazdu
                // nastepna pozycja = aktualna pozycja + predkosc
				x = j + t->V;
                // jezeli pojazd nie wyjedzie za krawedz wektora
				if (x < W)
				{
					y = 1;
                    // dopoki jestesmy w wektorze i sprawdzane komorki sa puste
                    // i y jest mniejsze od predkosci maksymalnej pojazdu
                    // tutaj liczymy ile komorek do przodu moze pojechac samochod
                    // faza zwalniania
					while (
						(j + y < W)
						&&
                        (d[i][j + y] == nullptr)
						&&
						(y < t->Vmax)
						)

					{
						y++;
					}
                    // jezeli y jest wieksze od aktualnej predkosci to zwieksz predkosc
                    if (y > t->V)
                        t->speedup();
                    // jezeli y jest mniejsze od aktualnej predkosci
                    // czyli przy aktualnej predkosci doszloby do kolizji
                    // to zwilnij do y, czyli do maksymalnej predkosci jaka
                    // moze osiagnac pojazd w takich warunkach (zwazajac na jego
                    // v_max oraz na ilosc wolnych komorek przed pojazdem)
                    else if (y < t->V)
                        t->V = y;

                    // przemieszczenie samochodu
					r[i][j + t->V] = t;
                    t = nullptr;
				}
				else
				{
                    // jezeli samochod wyjechal poza zakres usun
					delete t;
                    t = nullptr;
				}
			}
		}
	}
	delete[]d;
	d = r;
}


int main()
{
    srand(static_cast<unsigned int>(time(nullptr)));
    // tablica na 50 pojazdów
	pojazd **tabOb = new pojazd *[50];
    // wskaznik na dwie tablice pojazdow o dlugosci W=100
	pojazd ***d = new pojazd**[2];
    d[0] = new pojazd*[static_cast<unsigned long int>(W)];
    d[1] = new pojazd*[static_cast<unsigned long int>(W)];

	int nr = 0;
	int flaga = 0;

    // zerowanie tablicy wskaznikow
    // po kazdej tablicy w d
    for (int i = 0; i < 2; i++) {
        // po kazdym pojezdzie w wektorze
        for (int j = 0; j < W; j++) {
            // zerowanie wskaznikow
            d[i][j] = nullptr;
        }
    }

    // dopoki nie przepelni sie tablica obiektow (maksymalnie 50 samochodow)
	while (nr < 50) {
        // jezeli poczatek petli
		if (flaga == 0)
		{
			flaga = 6;
			nr++;
            // generuje nowy pojazd na poczatku wektora
            // tabOb przechowuje obiekty
			generator(d, tabOb[nr]);
		}
		else flaga--;
		wyswietlanie(d);
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
		system("cls");
		odswiezanie(d);
	}

	cout << endl;

	system("PAUSE");

	delete[]d;

	return 0;
}
