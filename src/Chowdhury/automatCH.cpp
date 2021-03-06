#include "Automat.h"
int main()
{
	// Output file
	std::ofstream file;
	// some info
	std::cout << "Automat chowdhury'ego" << std::endl;
	// start density value
	double density = 0.01;
	// ceil length
	const double ceil_len = 1.0;
	// cars number
	const int cars = 100;
	// temporary arraay for flows
	double tmp[2];
	// pointer to automat
	Automat *automat;

	// Otwieramy plik z flagami
	// out - plik wyjściowy ( zapis )
	// app - nadpisujemy na końcu pliku
	file.open("1,0.txt", std::ios::out | std::ios::trunc);
	// output data format info
	file << "Density;";
	//file << "Slow(0:100);Fast(0:100);";
	//file << "Slow(25:75);Fast(25:75);";
	file << "Slow(50:50);Fast(50:50);";
	//file << "Slow(75:25);Fast(75:25);";
	//file << "Slow(100:0);Fast(100:0);";
	file << std::endl;
		//Slow(0:100); Slow(0:)Fast(25:75); (50:50); (75:25); (100:0)" << std::endl;
	for (int i = 0; i < 50; i++) {
		// info
		std::cout << "[" << i + 1 << "] Iteration | Density: " << density << std::endl;
		// write actual density to file
		file << density;
		//for (int ratio = 0; ratio <= 100; ratio += 25) {
			// create new automat
			automat = new Automat(density, ceil_len, cars, 50);
			//automat->display = true;
			automat->Run();
			// read flow to a tmp
			automat->Data(tmp);
			// write flow to file
			// 0 - slow vehicles
			// 1 - fast vehicles
			file << ";" << tmp[0] << ";" << tmp[1];

			delete automat;
		//}
		// zapisujemy wartości 'density' oraz 'flow' oddzielone separatorem ';'
		file << std::endl;
		// increment density
		density += 0.01L;
	}
    return 0;
}

