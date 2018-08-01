import matplotlib.pyplot as plt
import time, sys

while True:

	file = open(sys.argv[1], 'r')
	dictionary = eval(file.read())
	plt.bar(range(len(dictionary)), list(dictionary.values()), align='center')
	plt.xticks(range(len(dictionary)), list(dictionary.keys()))
	plt.draw()
