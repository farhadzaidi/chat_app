def callFunction(func):
	def wrapper(*args, **kwargs):
		myName = func(*args, **kwargs)
		print('wrapper end')
		return myName

	return wrapper

@callFunction
def sayHello(name):
	return f'Hello {name}'

myName = sayHello('Farhad')
print(myName)