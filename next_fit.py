# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	count = 0
	i = 0
	while (i < len(items)):
		current = assignment[count]

		if (items[i] + current <= 1):
			assignment[count] += items[i]
		else:
			assignment[count + 1] += items[i]
			count += 1

		i += 1


bin = [.5, .7, .5, .2, .4, .2, .5, .1, .6]
assign = [0, 0, 0, 0, 0, 0, 0, 0, 0]
free = []

next_fit(bin, assign, free)

print(assign)
