#include "stdafx.h"

using namespace std;
static int W = 50;	//Dlugosc drogi
bool isChecked = false; //flaga , sprawdzamy czy dany pojazd byl aktualizowany podczas zmiany pasa
class pojazd
{
public:
	int V; //typ pojazdu
	int Vmax;// maksymalna predkosc pojazdu 
	int przydzial = 50; //Losowane pojazdy beda sie rozkladaly nastepujaco: p/100 = N;   (100-p)/100 = E;
	bool checked;// flaga sprawdzamy czy dany pojazd byl aktualizowany podczas zmiany pasa 
	pojazd() 
	{
		this->V = rand() % 100 + 1; //losowanie typu pojazdu
		this->checked = !isChecked;
	}
	void wyswietl() 
	{
		if (V <= przydzial)
			cout << "n";
		if (V > przydzial)
			cout << "e";
	}
};

void generator( pojazd ***&d)
{
	d[1][0] = new pojazd;
	d[0][0] = new pojazd;
}

void wyswietlanie(pojazd ***&d) {
	system("cls");
	for (int i = 0; i < W-1; i++) {
		for (int j = 0; j < W-1; j++) {
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
// Sprawdza czy samochod "n" moze sie przesunac do gory
bool CanIMoveNorth(pojazd ***d, int i, int j) {
	pojazd *t = d[i][j];
	if (d[i + 1][j] == nullptr)
	{
		//jesli pole nad pojazdem jest wolne to zwraca true
		return true;
	}
	else
	{
		return false;
	}
}
//Sprawdza czy samochod "e" moze sie przesunac w prawo
bool CanIMoveEast(pojazd ***d, int i, int j) {
	pojazd *t = d[i][j];
	if (d[i][j + 1] == nullptr)
	{
		//jesli pole na prawo od pojazdu jest wolne to zwraca true
		return true;
	}
	else
	{
		return false;
	}
}



void odswiezanie(pojazd ***&d)
{
	pojazd *t;
	int x, y;
	for (int i = 0, l = 1; i < W; i++, l--) {
		for (int j = 0; j < W; j++) {
			t = d[i][j];

			if (t != NULL && t->checked != isChecked)
			{
				t->checked = isChecked; //zmiana co cykl flagi
				if (t->V <= t->przydzial) //Sprawdzamy czy jest to samochod poruszajacy sie w gore
				{
					if (bool R = CanIMoveNorth(d, l, j) == true) //Sprawdzamy czy pozycja o 1 w gore od samochodu jest wolna
					{
						//Jesli tak, to przesuwamy samochod o 1 pole w gore
						d[l][j] = t;   
						d[i][j] = nullptr;
					}
					else
					{
						d[l][j] = nullptr;
					}
				}
				else if (t->V > t->przydzial) //Sprawdzamy czy jest to samochod poruszajacy sie w prawo
				{
					if (bool R = CanIMoveEast(d, l, j) == true)  //Sprawdzamy czy pozycja o 1 w prawo od samochodu jest wolna
					{
						//Jesli tak, to przesuwamy samochod o 1 pole w prawo
						d[i][l] = t;
						d[i][j] = nullptr;
					}
					else
					{
						d[i][l] = nullptr;
					}
				}
			}
		}
	}
					
				
			
		
	
	isChecked = !isChecked;

	/**/
	pojazd ***tmp = new pojazd**[2];
	for (int i = 0; i < W; i++) 
		{
		tmp[i] = new pojazd*[W];
		}
	for (int i = 0; i < 2; i++) { 
		for (int j = 0; j < W; j++) { tmp[i][j] = NULL; } }
	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < W; j++)
		{
			t = d[i][j];
			if (t != NULL)
			{
				//tutaj trzeba poprawic tez
				if (j < W) { tmp[i][j] = t; }
				else { delete t; }
				d[i][j] = NULL;
			}
		}
	}
	delete[]d;
	d = tmp;
	tmp = NULL;
}


int main()
{
	srand(time(NULL));
	pojazd ***d = new pojazd**[2];
	//Nie wiem jak generowac pojazdy, w sumie te ktore ida tylko w gore chyba powinny byc generowane tylko w ostatnim wierszu
	//a te ktore ida tylko w prawo powinny byc generowane tylko w pierwszej kolumnie??
	d[0] = new pojazd*[W];
	d[1] = new pojazd*[W];
	for (int i = 0; i < 2; i++) { for (int j = 0; j < W; j++) { d[i][j] = NULL; } }

	int nr = 0;
	int flaga = 0;

	while (nr<50) {
		if (flaga == 0)
		{
			flaga = 4;
			nr++;
			generator(d);
		}
		else flaga--;
		wyswietlanie(d);
		odswiezanie(d);
		Sleep(300);
	}
	cout << endl;
	system("PAUSE");
	delete []d;
    return 0;
}

