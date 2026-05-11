#import libary
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#read csv

door = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/door/doordelete.csv",skiprows=1)
prisoners = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/Prison/prisonersdelete.csv",skiprows=1)
metrix = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/Metrix/metrixdelete.csv",skiprows=1)
prime = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/interactive/prime/primedelete.csv",skiprows=1)
fibonacci = pd.read_csv("results/recursive/fibonacci/fibonaccidelete.csv",skiprows=1)
factorial = pd.read_csv("/home/keaw/github/Programming-Benchmark/results/recursive/factorial/factorialdelete.csv",skiprows=1)

label = door.columns[1:]


##read float
doorResult=door.iloc[0,1:].astype(float).values 
prisonersResult = prisoners.iloc[0,1:].astype(float).values
metrixResult = metrix.iloc[0,1:].astype(float).values
primeResult = prime.iloc[0,1:].astype(float).values
fibonacciResult= fibonacci.iloc[0,1:].astype(float).values
factorialResult = factorial.iloc[0,1:].astype(float).values 


def create_grapt(title,label,value):
    colors = []
    for i in label:
        if "BME."in i:
            colors.append("orange")
        elif "Dkr." in i:
            colors.append("blue")
    plt.figure(figsize=(14, 6))
    plt.title(title)
    bars=plt.bar(label,value,color=colors)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.3f}', 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.ylabel("Avg. Duration(s.)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.legend
    plt.show()


create_grapt("Door benchmark result(1,000,000 doors)",label,doorResult)
create_grapt("Metrix benchmark result(1000*1000 doors)",metrix.columns[1:],metrixResult)
create_grapt("Prisoners benchmark result(1,000,000 prisoners)",label,prisonersResult)
create_grapt("Prime number benchmark result(1000000 times)",label,primeResult)
create_grapt("Factorial benchmark result(100!)",label,factorialResult)
create_grapt("Fibonacci benchmark result(50)",label,fibonacciResult)


