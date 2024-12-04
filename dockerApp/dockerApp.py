import os
import time
import random
import relayService
from datetime import datetime

def bubble_sort(arr):
    # Sorts a list using the bubble sort algorithm and logs each step
    relayService.send_message_to_server(f"## Starting sorting algorithm: {datetime.now().strftime('%H:%M:%S')}")
    relayService.send_message_to_server(f"### Original list: {arr}: {datetime.now().strftime('%H:%M:%S')}")
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            relayService.send_message_to_server(f"-# Comparing {arr[j]} and {arr[j + 1]}: {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(3)
            if arr[j] > arr[j + 1]:
                # Swap items
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                relayService.send_message_to_server(f"Swapped {arr[j + 1]} and {arr[j]}: {arr}: {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(0.5)
    relayService.send_message_to_server(f"Finished sorting!")
    return arr

def create_rand_list(low_num, high_num):
    random_list = []
    while len(random_list) < 5:
        random_list.append(random.randint(int(low_num), int(high_num)))
    return random_list

if __name__ == "__main__":
    sample_list = create_rand_list(os.environ['LOW'], os.environ['HIGH'])
    sorted_list = bubble_sort(sample_list)
    relayService.send_message_to_server(f"Sorted list: {sorted_list}: {datetime.now().strftime('%H:%M:%S')}")