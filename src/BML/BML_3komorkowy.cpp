// BML.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <time.h>
#include <Windows.h>
using namespace std;
int MatrixSize = 45;
bool isChecked;
int probability = 45;   //w procentach

class pojazd
{
public:
	int CarType;   //1 - porusza sie w gore, 2 - porusza sie w prawo
	bool checked;
	pojazd()
	{
		this->checked = !isChecked;
	}
	
	void wyswietl()
	{
		if (CarType == 1)
			cout << "n";
		if (CarType == 2)
			cout << "e";
	}
};
/*
void FillMatrix(int MatrixSize, int wsk) {
	srand(time(NULL));
	for (int i = 0; i < MatrixSize; i++) {
		for (int j = 0; j < MatrixSize; j++) {
			int x = rand() % 2 + 1;
			if (x == 1)
			{
				*Matrix[i][j] = new pojazd;
			}
		}
	}
}
*/

int main()
{
	bool checkedE = FALSE;
	bool checkedN = FALSE;
	bool tick = FALSE;
	//generujemy tablice
	int **Matrix = new int *[MatrixSize];
	for (int i = 0; i < MatrixSize; i++)
	{
		Matrix[i] = new int[MatrixSize];
	}
	
	//generujemy tablice pomocnicza
	int **Matrix2 = new int *[MatrixSize];
	for (int i = 0; i < MatrixSize; i++)
	{
		Matrix2[i] = new int[MatrixSize];
	}
	
	for (int i = 0; i < MatrixSize; i++) {
		for (int j = 0; j < MatrixSize; j++) {
			Matrix2[i][j] = Matrix[i][j];
		}
	}



	srand(time(NULL));
	for (int i = 0; i < MatrixSize; i++) {
		for (int j = 0; j < MatrixSize; j++) {
			int y = rand() % 100 + 1; //losujemy czy dane pole bedzie puste czy nie
			if (y < probability) //Jesli w polu znajdzie sie samochod
			{
				
				int x = rand() % 2 + 1;   //losowanie jaki pojazd zostanie przypisany
				//if (x == 1)
				Matrix[i][j] = x;  //Jesli 1 to samochod przesuwa sie w gore, jesli 2 to w prawo
			}
			else
			{
				Matrix[i][j] = 0;  //Puste pole
			}
			
		}
	}
	while (1)
	{
		//Wyswietlanie Samochodow
		system("cls");
		for (int i = 0; i < MatrixSize; i++) {
			for (int j = 0; j < MatrixSize; j++) {
				if (Matrix[i][j] == 0)
				{
					cout << ". "; //Puste pole
				}
				else if (Matrix[i][j] == 1)
				{
					cout << "N "; //Samochod poruszajacy sie w gore
				}
				else if (Matrix[i][j] == 2)
				{
					cout << "E "; //Samochod poruszajacy sie w prawo
				}
			}
			cout << endl;
		}
		
		//Przesuwanie pojazdow
		if (tick == FALSE) //W tym przypadku ruszaja sie samochody idace w prawo
		{
			for (int i = MatrixSize - 1; i > -1; i--) {
				for (int j = MatrixSize - 1; j > -1; j--) {
					int k = j + 1; //Zmienna pomocnicza
					if (k == MatrixSize)
					{
						k = 0; //Jesli k wyjdzie poza zakres macierzy to zeruje k
					}
					if (Matrix2[i][j] == 2) //Jesli w danej komorce znajduje sie samochod jadacy w prawo
					{
						if (j == 0 && checkedE == TRUE)
						{
							Matrix2[i][j] == 2;
							checkedE = FALSE;
						}
						else if (Matrix2[i][k] == 0) //Jesli komorka na prawo od samochodu jest pusta
						{
							Matrix2[i][k] = 2; //Zapisujemy zmieniona pozycje samochodu w macierzy pomocniczej
							Matrix2[i][j] = 0; //Zwalniamy jego poprzednia pozycje w macierzy pomocniczej
							Matrix[i][j] = 0;
							//Matrix[i][k] = 2;
							if (k == 0)
							{
								checkedE = TRUE;
							}

						}
						else  //Jesli komorka na prawo od samochodu jest zajeta
						{
							Matrix2[i][j] = 2;  //Zapisujemy aktualna pozycje samochodu w macierzy pomocniczej
							//Matrix[i][j] = 2;
						}
					}
					else
					{
						Matrix2[i][j] = Matrix[i][j];
					}

				}
			}
		}
		if (tick == TRUE)
		{
			for (int i = 0; i < MatrixSize; i++) {
				for (int j = 0; j < MatrixSize; j++) {
					int k = i - 1; //Zmienna pomocnicza
					if (k < 0)
					{
						k = MatrixSize - 1; //Jesli k wyjdzie poza zakres macierzy to zeruje k
					}
					if (Matrix2[i][j] == 1) //Jesli w danej komorce znajduje sie samochod jadacy w gore
					{
						if (i == 0 && checkedN == TRUE)
						{
							Matrix2[i][j] == 1;
							checkedN = FALSE;
						}
						else if (Matrix2[k][j] == 0) //Jesli komorka na gorze od samochodu jest pusta
						{
							Matrix2[k][j] = 1; //Zapisujemy zmieniona pozycje samochodu w macierzy pomocniczej
							Matrix2[i][j] = 0; //Zwalniamy jego poprzednia pozycje w macierzy pomocniczej
							Matrix[i][j] = 0;
							if (k == MatrixSize - 1)
							{
								checkedN = TRUE;
							}

						}
						else  //Jesli komorka na gorze od samochodu jest zajeta
						{
							Matrix2[i][j] = 1;  //Zapisujemy aktualna pozycje samochodu w macierzy pomocniczej
												//Matrix[i][j] = 2;
						}
					}
					else
					{
						Matrix2[i][j] = Matrix[i][j];
					}

				}
			}
			
		}
		tick = !tick;
		//tick = !tick; //Zmieniamy rodzaj samochodow, ktore beda przesuwane w nastepnej iteracji
		
		
		for (int i = 0; i < MatrixSize; i++) {
			for (int j = 0; j < MatrixSize; j++) {
				//cout << Matrix[i][j];
				Matrix[i][j] = Matrix2[i][j];
				//cout << Matrix2[i][j] << "  ";

			}
		}
		

		Sleep(500);
	}

	/*int *wsk; // = &Matrix[MatrixSize][MatrixSize];
	wsk = &Matrix[MatrixSize][MatrixSize];

	FillMatrix(MatrixSize, *wsk);
	*/
	system("PAUSE");
    return 0;
}

