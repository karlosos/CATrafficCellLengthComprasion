#include "Automat.h"
#define FRONT	1
#define BACK	-1
Automat::Automat(double nDensity, double nCeilLen, int nCarNumb, int sVehicles) :
	density(nDensity),
	ceilLen(nCeilLen),
	carNumb(nCarNumb),
	//iterations(5*1000000),
	iterations(5000),
	currentIteration(0),
	flow{0,0},
	display(false){
	slowVehicles = sVehicles;
	fastVehicles = 100 - slowVehicles;
	GenerateVehicles();
	NewRoad(road);
	SetVehicle(0, carNumb / 2, 0);
	SetVehicle(carNumb / 2, carNumb, 1);
}
Automat::~Automat() {
	// Je�eli 'droga' istnieje
	if (road != NULL) {
		// Je�eli pierwszy pas 'drogi' istnieje
		if (road[0] != NULL) {
			// Zwalniamy pami��
			delete[] road[0];
			// Ustawiamy wska�nik na 'NULL'
			road[0] = NULL;
		}
		// Je�eli drugi pas 'drogi' istnieje
		if (road[1] != NULL) {
			// Zwalniamy pami��
			delete[] road[1];
			// Ustawiamy wska�nik na 'NULL'
			road[1] = NULL;
		}
		// Zwalniamy pami��
		delete[] road;
		// Ustawiamy wska�nik na 'NULL'
		road = NULL;
		// Je�eli tablica 'Pojazd�w' istnieje
		if (vehicle != NULL) {
			// Iterujemy po ka�dym z 'Pojazd�w'
			for (int i = 0; i < carNumb; i++) {
				// Je�eli aktualny 'Pojazd' istnieje
				if (vehicle[i] != NULL) {
					// Zwalniamy pami��
					delete vehicle[i];
					// Ustawiamy wska�nik na 'NULL'
					vehicle[i] = NULL;
				}
			}
			// Zwalniamy pami��
			delete[] vehicle;
			// Ustawiamy wska�nik na 'NULL'
			vehicle = NULL;
		}
	}
}
void Automat::Run() {
	// Dla ka�dej iteracji
	for (unsigned int i = 0; i < iterations; i++) {
		if (display) {
			// Czy�cimy konsol�
			system("cls");
			// Wy�wietlamy 'drog�'
			this->Display();
			// Czekamy 0.3 sec
			Sleep(300);
		}
		// Aktualizujemy stan 'drogi' -> 'Pojazd�w' na niej
		this->Update();
	}
	return;
}
void Automat::Data(double (&out)[2]) {
	// Warto�� 'flow'
	// slow vehicles
	out[0] = static_cast<double>(flow[0]) * density / static_cast<double>(iterations);
	// fast vehicles
	out[1] = static_cast<double>(flow[1]) * density / static_cast<double>(iterations);
	return;
}
void Automat::Update() {
	// Zmiana pasa
	Pojazd* t;
	// Luka przed pojazdem
	int frontGap;
	// Luka za pojazdem
	int backGap;
	// Reset avg speed
	avg[0] = 0.0;
	avg[1] = 0.0;
	// Iterujemy po pasach
	for (int i = 0, l = 1; i < 2; i++, l--) {
		// Iterujemy po kom�rkach
		for (int j = 0; j < ceilNumb; j++) {
			// Przypisujemy wska�nik na aktualny 'Pojazd'
			t = road[i][j];
			// Je�eli nie jest pusty
			if (t != NULL && !t->isChecked()) {
				//Zmieniamy stan 'Pojazdu' na nieodwiedzony
				t->setChecked(true);
				// Pozycja czo�a 'Pojazdu'
				int pos = t->GetHeadPosition();
				// Liczymy liczb� wolnych kom�rek z przodu pojazdu
				frontGap = Gap(i, pos, FRONT);
				// Je�eli  jest mniejsza ni� aktualna pr�dko�� 'Pojazdu'+1
				// LUB
				// Znajdujemy si� na g�rnym pasie
				if (frontGap < t->GetV() + 1 && frontGap < Gap(l, pos, FRONT)) {
					// Je�eli jest miejsce na zmian� pasa
					if (IsFreeSpace(t)) {
						// Obliczamy liczb� pustych kom�rek z ty�u pojazdu na drugim pasie
						backGap = Gap(l, t->GetTailPosition(), BACK);
						// Pozycja poprzedzaj�cego 'Pojazdu'
						pos = Position(t->GetTailPosition() - backGap - 1);
						// Je�eli backGap == ceilNumb  -> pusty pas
						// Je�eli liczba pustych  kom�rek na drugim pasie jest wi�ksza ni� pr�dko�� popredzaj�cego pojazdu
						if (backGap == ceilNumb || backGap > road[l][pos]->GetMaxV()) {
							// Zmieniamy pas
							ChangeLane(t);
						}
					}
				}
			}
		}
	}

	// Nowy stan drogi
	NewRoad(tmp);
	// Iterowanie po pasach
	for (int i = 0; i < 2; i++) {
		// Iterowanie po drodze
		for (int j = 0; j < ceilNumb; j++) {
			// Je�eli kom�rka nie jest pusta
			if (road[i][j] != NULL) {
				// Je�eli 'Pojazd' nie by� sprawdzany
				if (road[i][j]->isChecked()) {
					// Zaktualizuj pojazd
					UpdateVehicle(road[i][j]);
					// Collecting data
					if (road[i][j]->GetMaxV() == 3) {
						avg[0]+= road[i][j]->GetV();
					}
					else {
						avg[1] += road[i][j]->GetV();
					}
				}
				// Zapisujemy 'Pojazd' na nowej pozycji do tymczasowe 'drogi'
				tmp[i][Position(j + road[i][j]->GetV())] = road[i][j];
			}
		}
	}
	// Zwalniamy pami�� starej 'drogi'
	delete[] road[0];
	delete[] road[1];
	delete[] road;
	// Tymczasowa 'droga' staje si� nasz� obecn�
	road = tmp;
	// Czy�cimy wska�nik drogi tymczasowej
	tmp = NULL;
	// collect data
	if (slowVehicles != 0) 
		flow[0] += static_cast<double>(avg[0]) / static_cast<double>(slowVehicles);
	if (fastVehicles != 0)
		flow[1] += static_cast<double>(avg[1]) / static_cast<double>(fastVehicles);
}
void Automat::Display()
{
	// Dla ka�dego 'pasa'
	for (int i = 0; i < 2; i++) {
		// Dla ka�dej kom�rki na pasie
		for (int j = 0; j < ceilNumb; j++) {
			// Je�eli jest pusta
			if (road[i][j] == NULL) {
				// Wypisz '-'
				std::cout << "-";
			}
			// Je�eli jest zaj�ta przez 'Pojazd'
			else {
				// Wypisz jego pr�dko��
				std::cout<<road[i][j]->GetV();
			}
		}
		// Przej�cie do nowej linii ( kolejny pas )
		std::cout << std::endl;
	}
}
void Automat::GenerateVehicles() {
	// Komora maszyny losuj�cej jest pusta,
	// Nast�puje zwolnienie blokady
	// * maszyna si� kr�ci *
	srand(static_cast<unsigned int>(time(NULL)));
	// Liczba kom�rek zaj�tych przez wszytkie pojazdy na drodze
	int capacity = 0;
	// Rozk�ad pr�dko�ci pojazd�w
	std::vector<int> *speedVector = new std::vector<int>;
	// Liczba 'powolnych' pojazd�w
	int slowNumber = 50;
	// Liczba 'szybkich' pojazd�w
	int fastNumber = 50;

	// Rozmieszczamy pr�dko�ci w vetorze zgodnie z proporcj�
	for (int i = 0; i < slowNumber; i++) {
		// 'Powolne' pojazdy poruszaj� si� z pr�dko�ci� '3'
		speedVector->push_back(3);
	}
	for (int i = 0; i < fastNumber; i++) {
		// 'Szybkie' pojazdy poruszaj� si� z pr�dko�ci� '5'
		speedVector->push_back(5);
	}
	// Pr�dko�� pojazdu
	int v;
	// Wylosowany index
	int index;
	// Rozmiar 'Pojazdu' - liczba zaj�tych kom�rek
	int size;
	// Tworzymy tablic� 'Pojazd�w' o rozmiarze 'carNumb'
	vehicle = new Pojazd*[carNumb];
	for (int i = 0; i < carNumb; i++) {
		// Losujemy indeks z zakresu '0' - ' rozmiar speedVector'
		index = rand() % speedVector->size();
		// Pobieramy warto�� pr�dko�ci przypisan� do danego indeksu
		v = speedVector->at(index);
		// Usuwamy z vectora wylosowan� pr�dko��
		speedVector->erase(speedVector->begin() + index);
		// Losowanie dlugosci pojazu
		size = rand() % 3 + 2;
		// Obliczanie rozmiaru 'Pojazdu'
		size = static_cast<int>(ceil(static_cast<double>(size) / ceilLen));
		// Tworzymy pojazd z wylosowan� pr�dko�ci�
		vehicle[i] = new Pojazd(size, v);
		// Zliczamy liczb� kom�rek zaj�tych przez 'Pojazd'
		capacity += vehicle[i]->GetLength();
	}
	// Usuwamy vector
	speedVector->clear();
	delete speedVector;
	// Liczymy liczb� kom�rek automatu
	// Zaj�te kom�rki musz� stanowi� 'density' wszystkich kom�rek
	// Uwzgl�dniaj�c dodanie drugiego 'szybkiego' pasa,
	// Kt�ry w momencie uruchomienia symulacji jest pusty
	ceilNumb = static_cast<int>(ceil(static_cast<double>(capacity) / (density * 2.0)));
	//ceilNumb = static_cast<int>(ceil(static_cast<double>(capacity) / density));
}
void Automat::NewRoad(Pojazd***&r) {
	// Generujemy drog�
	r = new Pojazd**[2];
	// Tworymy pierwszy pas
	r[0] = new Pojazd*[ceilNumb];
	// Tworzymy drugi pas
	r[1] = new Pojazd*[ceilNumb];
	//
	for (int i = 0; i < ceilNumb; i++) {
		r[0][i] = NULL;
		r[1][i] = NULL;
	}
}
void Automat::SetVehicle(int start, int end, int lane) {
	// Rozmieszczamy 'Pojazdy' na 'drodze'
	// Pozycja 'Pojazdu'
	int pos = 0;
	// Iterujemy po 'Pojazdach'
	for (int i = start; i < end; i++) {
		// Ustaw pozycj� 'ogona' pojazdu
		vehicle[i]->SetTailPosition(pos);
		// Ustaw pas pojazdu
		vehicle[i]->SetLane(lane);
		// Dla kolejnych kom�rek 'Pojazdu'
		for (int posx = 0; posx < vehicle[i]->GetLength(); posx++, pos++) {
			// Zapisujemy je na aktualnej pozycji
			road[lane][pos] = vehicle[i];
		}
		// Ustaw pozycj� 'czo�a' pojazdu
		vehicle[i]->SetHeadPosition(pos - 1);
		// Odst�p mi�dzy kolejnym pojazdem
		pos++;
	}
}
void Automat::UpdateVehicle(Pojazd *&pojazd) {
	// Zmieniamy jego stan an 'sprawdzony'
	pojazd->setChecked(false);
	// Obliczamy liczbe pustych kom�rek z przody 'Pojazdu'
	int frontGap = Gap(pojazd->GetLane(), pojazd->GetHeadPosition(), FRONT);
	// Je�eli liczba kom�rk jest wi�ksza ni� nasza aktualna pr�dko��
	if (frontGap + 1 > pojazd->GetV() + 1) {
		// Przyspiesz
		pojazd->SpeedUp();
	}
	// Je�eli liczba kom�rek nie jest wi�ksza ni� nasza pr�dko��, i luka jest wi�ksza ni� 0
	if ( frontGap + 1 <= pojazd->GetV() ) {
		// Ustaw pr�dko�� r�wn� liczbie pustych kom�rek
		pojazd->SetV(frontGap);
	}
	// Prawdopodobie�stwo 0.25
	if (rand() % 100 < 10) {
		// Hamowanie
		pojazd->SpeedDown();
	}
	// Ustawiamy pozycj� czo�a pojazdu
	pojazd->SetHeadPosition(Position(pojazd->GetHeadPosition() + pojazd->GetV()));
	// Ustawiamy pozycj� ogona pojazdu
	pojazd->SetTailPosition(Position(pojazd->GetTailPosition() + pojazd->GetV()));
	// Sumujemy pr�dko�� aktualnego pojazdu do tablicy
}
bool Automat::IsFreeSpace(Pojazd *&pojazd){
	int lane = pojazd->GetLane() == 0 ? 1 : 0;
	int pos = pojazd->GetTailPosition();
	int head = pojazd->GetHeadPosition();
	do {
		if (road[lane][pos] != NULL) {
			return false;
		}
		pos = Position(pos + 1);
	} while (pos != head + 1);
	return true;
}
void Automat::ChangeLane(Pojazd *&pojazd){
	int lane = pojazd->GetLane() == 0 ? 1 : 0;
	int pos = pojazd->GetTailPosition();
	int head = pojazd->GetHeadPosition();
	do {
		road[lane][pos] = pojazd;
		road[pojazd->GetLane()][pos] = NULL;
		pos = Position(pos + 1);
	} while (pos != head + 1);
	pojazd->ChangeLane();
}
int Automat::Position(int pos) {
	// Je�eli pozycja wykracza poza wymiary drogi
	if (pos >= ceilNumb) {
		pos -= ceilNumb;
	}
	else if (pos < 0) {
		pos += ceilNumb;
	}
	return pos;
}
int Automat::Gap(int i, int j, int direction) {
	// Oblicza liczb� wolnych kom�rek z przody / ty�u pojazdu,
	// Kt�rego element znajduje si� na pozycji 'i' 'j'

	// Liczba pustych kom�rek
	int g = -1;
	// j - aktualnie sprawdzana pozycja na drodze
	do {
		// Przesuwamy si� o jedn� pozycj� w danym kierunku
		j = Position(j + direction);
		// Zwi�kszamy liczb� pustych kom�rek
		g++;
		// Dop�ki aktualny element drogi jest pusty
	} while (road[i][j] == NULL && g < ceilNumb);
	return g;
}