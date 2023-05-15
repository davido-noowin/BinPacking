import time
import argparse
import requirements
import random
import math
import csv
from collections.abc import Callable
from pathlib import Path


BIN_PACKING_ALGORITHMS = {
    'next_fit' : requirements.next_fit,
    'first_fit' : requirements.first_fit,
    'first_fit_decreasing' : requirements.first_fit_decreasing,
    'best_fit' : requirements.best_fit,
    'best_fit_decreasing' : requirements.best_fit_decreasing
}

DATA_DIRECTORY = Path('data')

parser = argparse.ArgumentParser(description= 'Benchmark Several Bin Packing Algorithms', 
                                 usage= 'benchmark.py [size] --algorithm [bin_packing_algorithm]')

parser.add_argument('size', type = int, help = 'The size of the list we want to put into bins')

parser.add_argument('--algorithm', choices = BIN_PACKING_ALGORITHMS.keys(), dest = 'algorithm_name',
                    help = 'The sorting algorithm to use', required = True)


def getDataPath( algorithm_name:str) -> Path:
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents = True, exist_ok = True)

    return (directory / algorithm_name).with_suffix('.csv')


def saveData(algorithm_name:str, size:int, waste:int):
    path = getDataPath(algorithm_name)

    with path.open('a', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([size, waste])


def generateList(size:int) -> list[float]:
    nums = [random.uniform(0.0, 0.7) for _ in range(size)]

    return nums


def benchmark(algorithm:Callable[[list[int]], None], size:int) -> None:
    nums = generateList(size)
    
    weight_of_list = sum(nums)
    num_of_bins = [0] * len(nums)
    free_space = []

    algorithm(nums, num_of_bins, free_space)

    waste = len(num_of_bins) - weight_of_list

    saveData(args.algorithm_name, size, waste)


if __name__ == '__main__':
    args = parser.parse_args()
    args.algorithm = BIN_PACKING_ALGORITHMS[args.algorithm_name]

    #for i in range(100):
    benchmark(args.algorithm, args.size)