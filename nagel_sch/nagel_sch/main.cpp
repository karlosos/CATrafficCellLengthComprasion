#include <stdio.h>
#include <tchar.h>
#include <iostream>
#include <Windows.h>
#include <time.h>

using namespace std;
static int W = 100;
static int VV = 3;
class pojazd
{
public:
	int V;
	int Vmax;
	//	int wielkosc;
	pojazd()
	{
		Vmax = rand() % 3 + 1;
		this->V = rand() % Vmax + 1;
	}

	void wyswietl() { cout << V; }

	void speedup() {
		if (V < Vmax) {
			V++;
		}
	}
	void speeddown() {
		if (V > 0) {
			V--;
		}
	}
};

void generator(pojazd ***&d, pojazd *&p)
{
	p = new pojazd;
	d[1][0] = p;
}

void wyswietlanie(pojazd ***&d) {

	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < W; j++) {
			if (d[i][j] == NULL)
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
	r[0] = new pojazd*[W];
	r[1] = new pojazd*[W];
	for (int i = 0; i < 2; i++) { for (int j = 0; j < W; j++) { r[i][j] = NULL; } }
	int x, y;
	for (int i = 0; i < 2; i++)
	{
		for (int j = 0; j < W; j++)
		{
			t = d[i][j];
			if (t != NULL)
			{
				x = j + t->V;
				if (x < W)
				{
					y = 1;
					while (
						(j + y < W)
						&&
						(d[i][j + y] == NULL)
						&&
						(y < t->Vmax)
						)

					{
						y++;
					}
					if (y > t->V) t->speedup();
					else if (y < t->V) t->V = y;

					r[i][j + t->V] = t;
					t = NULL;
				}
				else
				{
					delete t;
					t = NULL;
				}
			}
		}
	}
	delete[]d;
	d = r;
}


int main()
{
	srand(time(NULL));
	pojazd **tabOb = new pojazd *[50];
	pojazd ***d = new pojazd**[2];
	d[0] = new pojazd*[W];
	d[1] = new pojazd*[W];

	int nr = 0;
	int flaga = 0;

	for (int i = 0; i < 2; i++) { for (int j = 0; j < W; j++) { d[i][j] = NULL; } }

	while (nr < 50) {
		if (flaga == 0)
		{
			flaga = 6;
			nr++;
			generator(d, tabOb[nr]);
		}
		else flaga--;
		wyswietlanie(d);
		Sleep(200);
		system("cls");
		odswiezanie(d);
	}

	cout << endl;

	system("PAUSE");
	delete[]d;

	return 0;
}
