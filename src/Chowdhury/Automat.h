#pragma once

#include <vector>
#include <fstream>
#include <Windows.h>
#include <iostream>
#include <time.h>
#include "Pojazd.h"

// Automat dla Chowdhury'ego
class Automat {
public:
	// Czy wyœwietlamy stan drogi
	bool display;
private:
	// Gêstoœæ pojazdów na drodze
	double density;
	// Liczba komórek w drodze
	int ceilNumb;
	// Rzeczywista d³ugoœæ komórki
	double ceilLen;
	// Liczba pojazdów na drodze
	int carNumb;
	// Liczba iteracji symulacji
	unsigned int iterations;
	// Bie¿¹ca iteracja
	unsigned int currentIteration;
	// Flow of slow vehicles
	double flow[2];
	// avg speed of vehicles
	int avg[2];
	// Number of slow vehicles
	int slowVehicles;
	// Number of fast vehicles
	int fastVehicles;
	// Droga zbudowana z komórek - wskaŸników na elementy pojazdów
	Pojazd ***road;
	// Tablica wskaŸników na Pojazdy
	Pojazd **vehicle;
	// Zaktualizowana droga
	Pojazd ***tmp;
public:
	Automat(double, double, int, int);
	~Automat();
	void Run();
	void Data(double(&)[2]);
private:
	void Update();
	void Display();
	void GenerateVehicles();
	void NewRoad(Pojazd***&);
	void SetVehicle(int, int, int);
	void UpdateVehicle(Pojazd*&);
	bool IsFreeSpace(Pojazd*&);
	void ChangeLane(Pojazd*&);
	int Position(int);
	int Gap(int, int, int);
};