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
	// Je¿eli 'droga' istnieje
	if (road != NULL) {
		// Je¿eli pierwszy pas 'drogi' istnieje
		if (road[0] != NULL) {
			// Zwalniamy pamiêæ
			delete[] road[0];
			// Ustawiamy wskaŸnik na 'NULL'
			road[0] = NULL;
		}
		// Je¿eli drugi pas 'drogi' istnieje
		if (road[1] != NULL) {
			// Zwalniamy pamiêæ
			delete[] road[1];
			// Ustawiamy wskaŸnik na 'NULL'
			road[1] = NULL;
		}
		// Zwalniamy pamiêæ
		delete[] road;
		// Ustawiamy wskaŸnik na 'NULL'
		road = NULL;
		// Je¿eli tablica 'Pojazdów' istnieje
		if (vehicle != NULL) {
			// Iterujemy po ka¿dym z 'Pojazdów'
			for (int i = 0; i < carNumb; i++) {
				// Je¿eli aktualny 'Pojazd' istnieje
				if (vehicle[i] != NULL) {
					// Zwalniamy pamiêæ
					delete vehicle[i];
					// Ustawiamy wskaŸnik na 'NULL'
					vehicle[i] = NULL;
				}
			}
			// Zwalniamy pamiêæ
			delete[] vehicle;
			// Ustawiamy wskaŸnik na 'NULL'
			vehicle = NULL;
		}
	}
}
void Automat::Run() {
	// Dla ka¿dej iteracji
	for (unsigned int i = 0; i < iterations; i++) {
		if (display) {
			// Czyœcimy konsolê
			system("cls");
			// Wyœwietlamy 'drogê'
			this->Display();
			// Czekamy 0.3 sec
			Sleep(300);
		}
		// Aktualizujemy stan 'drogi' -> 'Pojazdów' na niej
		this->Update();
	}
	return;
}
void Automat::Data(double (&out)[2]) {
	// Wartoœæ 'flow'
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
		// Iterujemy po komórkach
		for (int j = 0; j < ceilNumb; j++) {
			// Przypisujemy wskaŸnik na aktualny 'Pojazd'
			t = road[i][j];
			// Je¿eli nie jest pusty
			if (t != NULL && !t->isChecked()) {
				//Zmieniamy stan 'Pojazdu' na nieodwiedzony
				t->setChecked(true);
				// Pozycja czo³a 'Pojazdu'
				int pos = t->GetHeadPosition();
				// Liczymy liczbê wolnych komórek z przodu pojazdu
				frontGap = Gap(i, pos, FRONT);
				// Je¿eli  jest mniejsza ni¿ aktualna prêdkoœæ 'Pojazdu'+1
				// LUB
				// Znajdujemy siê na górnym pasie
				if (frontGap < t->GetV() + 1 && frontGap < Gap(l, pos, FRONT)) {
					// Je¿eli jest miejsce na zmianê pasa
					if (IsFreeSpace(t)) {
						// Obliczamy liczbê pustych komórek z ty³u pojazdu na drugim pasie
						backGap = Gap(l, t->GetTailPosition(), BACK);
						// Pozycja poprzedzaj¹cego 'Pojazdu'
						pos = Position(t->GetTailPosition() - backGap - 1);
						// Je¿eli backGap == ceilNumb  -> pusty pas
						// Je¿eli liczba pustych  komórek na drugim pasie jest wiêksza ni¿ prêdkoœæ popredzaj¹cego pojazdu
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
			// Je¿eli komórka nie jest pusta
			if (road[i][j] != NULL) {
				// Je¿eli 'Pojazd' nie by³ sprawdzany
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
	// Zwalniamy pamiêæ starej 'drogi'
	delete[] road[0];
	delete[] road[1];
	delete[] road;
	// Tymczasowa 'droga' staje siê nasz¹ obecn¹
	road = tmp;
	// Czyœcimy wskaŸnik drogi tymczasowej
	tmp = NULL;
	// collect data
	if (slowVehicles != 0) 
		flow[0] += static_cast<double>(avg[0]) / static_cast<double>(slowVehicles);
	if (fastVehicles != 0)
		flow[1] += static_cast<double>(avg[1]) / static_cast<double>(fastVehicles);
}
void Automat::Display()
{
	// Dla ka¿dego 'pasa'
	for (int i = 0; i < 2; i++) {
		// Dla ka¿dej komórki na pasie
		for (int j = 0; j < ceilNumb; j++) {
			// Je¿eli jest pusta
			if (road[i][j] == NULL) {
				// Wypisz '-'
				std::cout << "-";
			}
			// Je¿eli jest zajêta przez 'Pojazd'
			else {
				// Wypisz jego prêdkoœæ
				std::cout<<road[i][j]->GetV();
			}
		}
		// Przejœcie do nowej linii ( kolejny pas )
		std::cout << std::endl;
	}
}
void Automat::GenerateVehicles() {
	// Komora maszyny losuj¹cej jest pusta,
	// Nastêpuje zwolnienie blokady
	// * maszyna siê krêci *
	srand(static_cast<unsigned int>(time(NULL)));
	// Liczba komórek zajêtych przez wszytkie pojazdy na drodze
	int capacity = 0;
	// Rozk³ad prêdkoœci pojazdów
	std::vector<int> *speedVector = new std::vector<int>;
	// Liczba 'powolnych' pojazdów
	int slowNumber = 50;
	// Liczba 'szybkich' pojazdów
	int fastNumber = 50;

	// Rozmieszczamy prêdkoœci w vetorze zgodnie z proporcj¹
	for (int i = 0; i < slowNumber; i++) {
		// 'Powolne' pojazdy poruszaj¹ siê z prêdkoœci¹ '3'
		speedVector->push_back(3);
	}
	for (int i = 0; i < fastNumber; i++) {
		// 'Szybkie' pojazdy poruszaj¹ siê z prêdkoœci¹ '5'
		speedVector->push_back(5);
	}
	// Prêdkoœæ pojazdu
	int v;
	// Wylosowany index
	int index;
	// Rozmiar 'Pojazdu' - liczba zajêtych komórek
	int size;
	// Tworzymy tablicê 'Pojazdów' o rozmiarze 'carNumb'
	vehicle = new Pojazd*[carNumb];
	for (int i = 0; i < carNumb; i++) {
		// Losujemy indeks z zakresu '0' - ' rozmiar speedVector'
		index = rand() % speedVector->size();
		// Pobieramy wartoœæ prêdkoœci przypisan¹ do danego indeksu
		v = speedVector->at(index);
		// Usuwamy z vectora wylosowan¹ prêdkoœæ
		speedVector->erase(speedVector->begin() + index);
		// Losowanie dlugosci pojazu
		size = rand() % 3 + 2;
		// Obliczanie rozmiaru 'Pojazdu'
		size = static_cast<int>(ceil(static_cast<double>(size) / ceilLen));
		// Tworzymy pojazd z wylosowan¹ prêdkoœci¹
		vehicle[i] = new Pojazd(size, v);
		// Zliczamy liczbê komórek zajêtych przez 'Pojazd'
		capacity += vehicle[i]->GetLength();
	}
	// Usuwamy vector
	speedVector->clear();
	delete speedVector;
	// Liczymy liczbê komórek automatu
	// Zajête komórki musz¹ stanowiæ 'density' wszystkich komórek
	// Uwzglêdniaj¹c dodanie drugiego 'szybkiego' pasa,
	// Który w momencie uruchomienia symulacji jest pusty
	ceilNumb = static_cast<int>(ceil(static_cast<double>(capacity) / (density * 2.0)));
	//ceilNumb = static_cast<int>(ceil(static_cast<double>(capacity) / density));
}
void Automat::NewRoad(Pojazd***&r) {
	// Generujemy drogê
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
		// Ustaw pozycjê 'ogona' pojazdu
		vehicle[i]->SetTailPosition(pos);
		// Ustaw pas pojazdu
		vehicle[i]->SetLane(lane);
		// Dla kolejnych komórek 'Pojazdu'
		for (int posx = 0; posx < vehicle[i]->GetLength(); posx++, pos++) {
			// Zapisujemy je na aktualnej pozycji
			road[lane][pos] = vehicle[i];
		}
		// Ustaw pozycjê 'czo³a' pojazdu
		vehicle[i]->SetHeadPosition(pos - 1);
		// Odstêp miêdzy kolejnym pojazdem
		pos++;
	}
}
void Automat::UpdateVehicle(Pojazd *&pojazd) {
	// Zmieniamy jego stan an 'sprawdzony'
	pojazd->setChecked(false);
	// Obliczamy liczbe pustych komórek z przody 'Pojazdu'
	int frontGap = Gap(pojazd->GetLane(), pojazd->GetHeadPosition(), FRONT);
	// Je¿eli liczba komórk jest wiêksza ni¿ nasza aktualna prêdkoœæ
	if (frontGap + 1 > pojazd->GetV() + 1) {
		// Przyspiesz
		pojazd->SpeedUp();
	}
	// Je¿eli liczba komórek nie jest wiêksza ni¿ nasza prêdkoœæ, i luka jest wiêksza ni¿ 0
	if ( frontGap + 1 <= pojazd->GetV() ) {
		// Ustaw prêdkoœæ równ¹ liczbie pustych komórek
		pojazd->SetV(frontGap);
	}
	// Prawdopodobieñstwo 0.25
	if (rand() % 100 < 10) {
		// Hamowanie
		pojazd->SpeedDown();
	}
	// Ustawiamy pozycjê czo³a pojazdu
	pojazd->SetHeadPosition(Position(pojazd->GetHeadPosition() + pojazd->GetV()));
	// Ustawiamy pozycjê ogona pojazdu
	pojazd->SetTailPosition(Position(pojazd->GetTailPosition() + pojazd->GetV()));
	// Sumujemy prêdkoœæ aktualnego pojazdu do tablicy
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
	// Je¿eli pozycja wykracza poza wymiary drogi
	if (pos >= ceilNumb) {
		pos -= ceilNumb;
	}
	else if (pos < 0) {
		pos += ceilNumb;
	}
	return pos;
}
int Automat::Gap(int i, int j, int direction) {
	// Oblicza liczbê wolnych komórek z przody / ty³u pojazdu,
	// Którego element znajduje siê na pozycji 'i' 'j'

	// Liczba pustych komórek
	int g = -1;
	// j - aktualnie sprawdzana pozycja na drodze
	do {
		// Przesuwamy siê o jedn¹ pozycjê w danym kierunku
		j = Position(j + direction);
		// Zwiêkszamy liczbê pustych komórek
		g++;
		// Dopóki aktualny element drogi jest pusty
	} while (road[i][j] == NULL && g < ceilNumb);
	return g;
}