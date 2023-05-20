import matplotlib.pyplot as plt
import numpy
import csv
from collections import defaultdict
from pathlib import Path

DATA_DIRECTORY = Path('CS161\\BinPacking\\data')


def getDataPath( algorithm_name:str) -> Path:
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents = True, exist_ok = True)

    return (directory / algorithm_name).with_suffix('.csv')


def loadData(algorithm_name:str) -> dict[int, list[int]]:
    path = getDataPath(algorithm_name)
    print(path)

    data = defaultdict(list)
    with path.open() as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            data[int(row[0])].append(float(row[1]))

    return data


def loadAverageData(algorithm_name:str) -> tuple[list[int], list[int]]:
    data = loadData(algorithm_name)
    sizes = []
    average_waste = []

    for size, waste in sorted(data.items()):
        sizes.append(size)
        average_waste.append(sum(waste) / len(waste))

    return sizes, average_waste


def addToPlot(algorithm_name:str, color:str):
    sizes, average_times = loadAverageData(algorithm_name)

    x,y = sizes[5:], average_times[5:] # might have to change
    logx, logy = numpy.log(x), numpy.log(y)

    # making a best fit line
    m, b = numpy.polyfit(logx, logy, 1)
    fit = numpy.poly1d((m, b))

    plt.loglog(sizes, average_times, '.', base = 2, color = color, label = '_hide')

    expected_y = fit(logx)

    
    # plotting the line of best fit
    equation = f'{algorithm_name}: log C(n) ~ {numpy.round(m, 5)} log n + {numpy.round(b, 5)})'
    plt.loglog(x, numpy.exp(expected_y), base = 2, color = color, label = equation)

    #plt.text(2**9, y[-1], equation).set_color(color)
    plt.xlabel('Input Size (n, # of elements)')
    plt.ylabel('Waste (# bins used - sum of items)')
    plt.title(f'{algorithm_name.capitalize()}')
    
    return equation


if __name__ == '__main__':
    e0 = addToPlot('first_fit', 'green')

    plt.show()