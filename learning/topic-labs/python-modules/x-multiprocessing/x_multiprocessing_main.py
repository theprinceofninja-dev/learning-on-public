import multiprocessing
import os
import time


def process_file(filename):
    """Process a single file"""
    print(f"Starting Processing {filename} in process {os.getpid()}")
    time.sleep(10)
    # Your processing logic here
    return f"Done Processing {filename}"


if __name__ == "__main__":
    files = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt",
        "file5.txt",
        "file6.txt",
        "file7.txt",
        "file8.txt",
    ]

    with multiprocessing.Pool(processes=8) as pool:
        results = pool.map(process_file, files)

    print("Results:", results)
