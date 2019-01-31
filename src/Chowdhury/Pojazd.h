#pragma once
class Pojazd {
private:
	// Aktualna pr�dko�� pojazdu
	int v;
	// Maksymalna pr�dko�� pojazdu
	int vMax;
	// D�ugo�� 'Pojazdu' w kom�rkach
	int carLen;
	// Pozycja czo�� 'g�owy' pojazdu
	int head;
	// Pozycja ty�u 'ogona' pojazdu
	int tail;
	// Pas po kt�rym si� porusza pojazd
	int lane;
	// Czy 'Pojazd' by� ju� sprawdzany
	bool checked;
public:
	Pojazd(int, int);
	int GetLength();
	int GetV();
	void SetV(int);
	int GetMaxV();
	int GetHeadPosition();
	void SetHeadPosition(int);
	int GetTailPosition();
	void SetTailPosition(int);
	int GetLane();
	void SetLane(int);
	void ChangeLane();
	bool isChecked();
	void setChecked(bool);
	void SpeedUp();
	void SpeedDown();
};
