#import libary
import matplotlib as plt
import numpy as np
import pandas as pd

#read csv

door = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/door/doordelete.csv")
prisoners = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/Prison/prisonersdelete.csv")
metrix = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/Metrix/metrixdelete.csv")
prime = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/prime/primedelete.csv")
fibonacci = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/recursive/factorial/factorialdelete.csv")
factorial = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/recursive/fibonacci/fibonaccidelete.csv")

print(door.iloc[0:2])