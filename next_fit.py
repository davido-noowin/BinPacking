# Example file: next_fit.py
import sys
import decimal
# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	count = 0
	i = 0
	
	precision = decimal.Context(prec=20)

	free_space.append(1)
	while (i < len(items)):
		current = free_space[count]

		if (current - items[i] >= -sys.float_info.epsilon):
			assignment[i] = count
			free_space[count] -= items[i]
		else:
			free_space.append(1)
			count += 1
			assignment[i] = count
			free_space[count] -= items[i]

		i += 1

	for i in range(len(free_space)):
		remain = decimal.Decimal(free_space[i])
		modded = remain.quantize(decimal.Decimal('.000000000000001'), context=precision)
		free_space[i] = float(modded.normalize())

'''
bin = [0.1, 0.8, 0.3, 0.5, 0.7, 0.2, 0.6, 0.4]
assign = [0, 0, 0, 0, 0, 0, 0, 0]
free = []

next_fit(bin, assign, free)

print(assign)
print(free)
'''