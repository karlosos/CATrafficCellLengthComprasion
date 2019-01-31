#pragma once
class Model
{
public:
	Model();
	~Model();
	virtual void Update()=0;
};

class Nagel : public Model {
public:
	void Update();
};
class STCA : public Model {
public :
	void Update();
};