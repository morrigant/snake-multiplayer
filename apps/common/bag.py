from random import randint

def randint_se(min, max, exc):
	number = randint(min, max)
	
	while number in exc:
		number = randint(min, max)

	return number

