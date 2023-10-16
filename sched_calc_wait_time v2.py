#! /usr/bin/env python3
# sched-calc-wait-time.py

### Código hecho por Matías Di Palma y Gaspar Morales, 16/10/2023
"""
El código recibe una lista de procesos y devuelve los tiempos de espera por proceso y el tiempo de espera promedio.
Permite calcularlos usando tres algoritmos: Round Robin (RR), Shortest Job First (SJF) también conocido como Shortest
Process Next (SPN) y First Come First Serve (FCFS) también conocido como First In First Out (FIFO)
"""

import argparse
import sys

"Se añade la librería deque"
from collections import deque

#RR Da un valor correcto, completado
def round_robin(processes, arrival_times, burst_times, quantum):
    """
    Calculate waiting times for processes using the Round Robin scheduling algorithm.

    :param processes: List of process identifiers.
    :param arrival_times: List of arrival times for each process.
    :param burst_times: List of burst times (duration) for each process.
    :param quantum: Time quantum for the RR scheduling.
    :return: List of waiting times for each process.
    """
    # TODO: Implement the RR algorithm

    n = len(processes)
    # Create a list to store the remaining burst times for each process
    remaining_burst_times = list(burst_times)
    # Create a list to store the waiting times for each process
    waiting_times = [0] * n
    # Create a variable to keep track of the current time
    current_time = 0

    while True:
        # Create a flag to check if all processes have completed
        all_completed = True
        for i in range(n):
            if remaining_burst_times[i] > 0:
                all_completed = False
                if remaining_burst_times[i] > quantum:
                    # Process runs for a time quantum
                    current_time += quantum
                    remaining_burst_times[i] -= quantum
                else:
                    # Process completes its execution
                    current_time += remaining_burst_times[i]
                    waiting_times[i] = current_time - arrival_times[i] - burst_times[i]
                    remaining_burst_times[i] = 0

        # If all processes have completed, exit the loop
        if all_completed:
            break

    return waiting_times

#SJF Da un valor correcto, completado
def sjf(processes, arrival_times, burst_times):
    """
    Calculate waiting times for processes using the Shortest Job First scheduling algorithm.

    :param processes: List of process identifiers.
    :param arrival_times: List of arrival times for each process.
    :param burst_times: List of burst times (duration) for each process.
    :return: List of waiting times for each process.
    """
    # TODO: Implement the SJF algorithm

    n = len(processes)
    # Create a list to store the waiting times for each process
    waiting_times = [0] * n
    # Create a list to keep track of whether a process has been completed or not
    completed = [False] * n
    # Initialize the total time to 0
    total_time = 0
    # Create a variable to keep track of the number of completed processes
    completed_processes = 0

    while completed_processes < n:
        # Find the index of the next process with the shortest remaining burst time
        min_burst_time = float('inf')
        min_index = -1
        for i in range(n):
            if not completed[i] and arrival_times[i] <= total_time and burst_times[i] < min_burst_time:
                min_burst_time = burst_times[i]
                min_index = i

        # If no process is found, increment the total time
        if min_index == -1:
            total_time += 1
        else:
            # Update waiting time for the selected process
            waiting_times[min_index] = total_time - arrival_times[min_index]
            # Update total time
            total_time += burst_times[min_index]
            # Mark the process as completed
            completed[min_index] = True
            completed_processes += 1

    return waiting_times

#FCFS Da un valor correcto, completado
def fcfs(processes, arrival_times, burst_times):
    """
    Calculate waiting times for processes using the First Come First Serve scheduling algorithm.

    :param processes: List of process identifiers.
    :param arrival_times: List of arrival times for each process.
    :param burst_times: List of burst times (duration) for each process.
    :return: List of waiting times for each process.
    """
    # TODO: Implement the FCFS algorithm

    n = len(processes)
    completion_times = [0] * n
    waiting_times = [0] * n

    for i in range(1, n):
        completion_times[i] = completion_times[i - 1] + burst_times[i - 1]

    for i in range(n):
        waiting_times[i] = completion_times[i] - arrival_times[i]

    return waiting_times

    return [3,3,3]

def calculate_waiting_times(algorithm, processes, arrival_times, burst_times, quantum=None):
    if algorithm == 'rr':
        return round_robin(processes, arrival_times, burst_times, quantum)
    elif algorithm == 'sjf':
        return sjf(processes, arrival_times, burst_times)
    elif algorithm == 'fcfs':
        return fcfs(processes, arrival_times, burst_times)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate waiting times for various scheduling algorithms.")

    parser.add_argument("-f", "--filename", help="Input file containing process data in the format: process_id, arrival_time, burst_time. If not provided, will read from standard input.")
    parser.add_argument("-q", "--quantum", type=int, help="Time quantum for RR scheduling. Required if algorithm is 'rr'.")
    parser.add_argument("-a", "--algorithm", choices=["rr", "sjf", "fcfs"], required=True, help="Scheduling algorithm to use.")

    args = parser.parse_args()

    processes, arrival_times, burst_times = [], [], []
    # Load data from file or standard input
    source = open(args.filename, 'r') if args.filename else sys.stdin

    if args.algorithm == 'rr' and args.quantum is None:
        parser.error("Quantum is required for RR scheduling.")

    if not args.filename:
        print("Ingrese las líneas que describen al nombre del proceso, su momento de llegada y su duración, en números enteros, separadas con espacio.\nFinalice con Control-D luego de entrar la última línea.", file=sys.stderr)

    for line in source:
        process, arrival, burst = line.strip().split()
        processes.append(process)
        arrival_times.append(int(arrival))
        burst_times.append(int(burst))
    if source != sys.stdin:
        source.close()

    waiting_times = calculate_waiting_times(args.algorithm, processes, arrival_times, burst_times, args.quantum)
    average_waiting_time = sum(waiting_times) / len(waiting_times)

    print(f"Waiting Times for {processes}: {waiting_times}")
    print(f"Average Waiting Time: {average_waiting_time:.2f}")

