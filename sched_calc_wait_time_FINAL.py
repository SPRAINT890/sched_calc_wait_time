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
    # Crea una lista para almacenar los tiempos restantes
    remaining_burst_times = list(burst_times)
    # Crea una lista para almacenar los tiempos de espera de cada proceso
    waiting_times = [0] * n
    # Crea una variable para mantener una cuenta del tiempo que pasa
    current_time = 0

    while True:
        # Flag para verificar que se completaron todos los procesos
        all_completed = True
        for i in range(n):
            if remaining_burst_times[i] > 0:
                all_completed = False
                if remaining_burst_times[i] > quantum:
                    # Se correo el proceso por el quantum determinado
                    current_time += quantum
                    remaining_burst_times[i] -= quantum
                else:
                    # Se completa el proceso
                    current_time += remaining_burst_times[i]
                    waiting_times[i] = current_time - arrival_times[i] - burst_times[i]
                    remaining_burst_times[i] = 0

        # Si se completaron todos los procesos termina el loop
        if all_completed:
            break

    # Devuelve los tiempos de espera
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
    # Crea una lista para almacenar los tiempos de espera de cada proceso
    waiting_times = [0] * n
    # Crea una lista para almacenar los procesos que se completaron
    completed = [False] * n
    # Se inicializa una variable de tiempo en 0
    total_time = 0
    # Se crea una variable para medir los procesos completados
    completed_processes = 0

    while completed_processes < n:
        # Se busca el proceso restante con el menor tiempo de duración
        min_burst_time = float('inf')
        min_index = -1
        for i in range(n):
            if not completed[i] and arrival_times[i] <= total_time and burst_times[i] < min_burst_time:
                min_burst_time = burst_times[i]
                min_index = i

        # Si no se encuentra uno se incrementa el tiempo total
        if min_index == -1:
            total_time += 1
        else:
            # Actualiza el tiempo de espera para el proceso actual
            waiting_times[min_index] = total_time - arrival_times[min_index]
            # Actualiza el tiempo total
            total_time += burst_times[min_index]
            # Completa el proceso
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

    #Se crea una lista para almacenar los tiempos de completado de los procesos
    completion_times = [0] * n

    #Se crea una lista para almacenar los tiempos de espera de los procesos
    waiting_times = [0] * n

    #Calcula el tiempo de completado
    for i in range(1, n):
        completion_times[i] = completion_times[i - 1] + burst_times[i - 1]

    #Almacena el tiempo de espera
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

