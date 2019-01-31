#pragma once
class Pojazd {
private:
	// Aktualna prêdkoœæ pojazdu
	int v;
	// Maksymalna prêdkoœæ pojazdu
	int vMax;
	// D³ugoœæ 'Pojazdu' w komórkach
	int carLen;
	// Pozycja czo³¹ 'g³owy' pojazdu
	int head;
	// Pozycja ty³u 'ogona' pojazdu
	int tail;
	// Pas po którym siê porusza pojazd
	int lane;
	// Czy 'Pojazd' by³ ju¿ sprawdzany
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
