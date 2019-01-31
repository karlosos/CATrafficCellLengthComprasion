#include "Model.h"
Model::Model(){}
Model::~Model(){}

Nagel::Nagel() {};
Nagel::~Nagel() {};
void Nagel::Update() {
	/*
	One dimensional array of L sites

	V: 0-Vmax

	Update:
		1) Acceleration:
			if ( V < Vmax ) && ( gap(front) > V + 1 )
			[ gap(front) -> distance to the next car ahead ]
			[ NOT NUMBER OF EMPTY CELLS! ]
		2) Slowing down ( due to other cars ):
			i	- position of current vehicle
			i+j	- position of next vehicle

			if ( j<=V ): V = V - 1
		3) Randomization:
			With probability ( p ):
				if (V>0): V = V - 1
		4) Car motion:
			each vehicle is advanced v sites


	'Realistic case':
		Vmax = 5

				number of cars in the circle
	Density		-----------------------------
				number of sites of the circle

	Each car occupies about 7.5m of placec
	Length of one site = 7.5m
	Average V in the free traffic of 4.5 sites / time step ==> 120km/h

	time_step ~ 1.0125 sec

	Av. flow q [ # of cars per time step ]

	- When site 1 is empty: occupy it with a car of v=0
	- The last 6 sites: delete cars

	Grid length up to 10'000 sites,
	5 x 10^6 time steps



	Freeways have a maximum capacity of about:
			2'000 vehicles / hour and lane = 0.56 vehicle / sec 
	*/
}
void STCA::Update() {
	/*


	LANE CHANGING RULES:
		1) if ( frontGapCurrent < V + 1 )
						&&
		2) if ( frontGapOther   > frontGapCurrent )
						&&
		3) The nearest neighbor site in the other lane is empty
					&&
		4) The maximal possible speed of the vehicle behind
			in the other lane is smaller than the gap in between

		V - current velocity
		All vehicles have the same Vmax
	




	NOTE:
	[frontGap]: the gap in front of vehicle
				number of empty cells between next vehicle
	
	1) if ( V < Vmax ) : V++
	2) if ( V > [frontGap] - 1 ): V = [frontGap] - 1
	3) if (V > 0) && ( rand()< p ): V--
	4) X(n) = X(n) + V
	
	*/
}
