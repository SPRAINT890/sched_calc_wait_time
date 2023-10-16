#! /usr/bin/env python3
# sched-calc-wait-time.py


import argparse
import sys

"Se añade la librería deque"
import collections 

def round_robin(processes, arrival_times, burst_times, quantum):
    """
    Calculate waiting times for processes using the Round Robin scheduling algorithm.
    :param processes: List of process identifiers.
    :param arrival_times: List of arrival times for each process.
    :param burst_times: List of burst times (duration) for each process.
    :param quantum: Time quantum for the RR scheduling.
    :return: List of waiting times for each process.
    """
    numCicles = 0
    totalNumCicles = 0 #ciclos ejecutados desde el inicio del programa
    waiting_times = [] #lista de tiempo de espera de cada proceso
    burst_times_linkedList = collections.deque()
    waiting_times_linkedlist = collections.deque()
    completo = False
    
    
    for i in range(len(processes)):
        burst_times_linkedList.append(burst_times[i])
        waiting_times_linkedlist.append(0)
    
    while True:
        if numCicles == quantum and totalNumCicles != 0 or completo:
            completo = False
            numCicles = 0
            burst_times_linkedList.rotate(-1)
            waiting_times_linkedlist.rotate(-1)
            waiting_times_linkedlist[0] = totalNumCicles-waiting_times_linkedlist[0]-1
        burst_times_linkedList[0]-=1
        if burst_times_linkedList[0] == 0:
            burst_times_linkedList.popleft()
            waiting_times.append(waiting_times_linkedlist.popleft())
            completo = True
            if len(burst_times_linkedList) == 0:
                break
        totalNumCicles+=1
        numCicles += 1
    
    for i in range(len(processes)):
        waiting_times[i] -= arrival_times[i]
    return waiting_times

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
    completion_times = [0] * n
    waiting_times = [0] * n
    remaining_time = list(burst_times)
    for time in range(max(arrival_times), sum(burst_times) + max(arrival_times)):
        min_burst_time = float('inf')
        shortest = -1
        for i in range(n):
            if arrival_times[i] <= time and remaining_time[i] < min_burst_time and remaining_time[i] > 0:
                min_burst_time = remaining_time[i]
                shortest = i
        if shortest == -1:
            continue
        remaining_time[shortest] = 0
        completion_times[shortest] = time + 1
        waiting_times[shortest] = completion_times[shortest] - arrival_times[shortest] - burst_times[shortest]

    return waiting_times

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

