#include "Pojazd.h"

Pojazd::Pojazd(int nCarLen, int nV) :
	vMax(nV),
	carLen(nCarLen),
	v(nV),
	checked(false){
}
int Pojazd::GetV(){
	return this->v;
}
int Pojazd::GetLength() {
	return this->carLen;
}
int Pojazd::GetMaxV() {
	return this->vMax;
}
int Pojazd::GetHeadPosition(){
	return this->head;
}
void Pojazd::SetHeadPosition(int pos) {
	this->head = pos;
}
int Pojazd::GetTailPosition(){
	return this->tail;
}
void Pojazd::SetTailPosition(int pos) {
	this->tail = pos;
}
int Pojazd::GetLane(){
	return this->lane;
}
void Pojazd::SetLane(int nLane){
	this->lane = nLane;
}
void Pojazd::ChangeLane(){
	this->lane = (lane == 0) ? 1 : 0;
}
void Pojazd::SetV(int nV) {
	this->v = nV;
}
bool Pojazd::isChecked() {
	return this->checked;
}
void Pojazd::setChecked(bool state) {
	this->checked = state;
}
void Pojazd::SpeedUp() {
	this->v++;
	if (this->v > this->vMax) {
		this->v = this->vMax;
	}
}
void Pojazd::SpeedDown() {
	this->v--;
	if (this->v < 0) {
		this->v = 0;
	}
}