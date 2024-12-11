from multiprocessing import Process, Queue
from .fdtool.fdtool import main


def run_fdtool(df, max_time=5, max_k_level=10):
    result_queue = Queue()
    process = Process(target=main, args=(result_queue, df, max_k_level))
    process.start()

    process.join(timeout=max_time)

    # If process is still active
    if process.is_alive():
        print("\nExceeded preset time limit.")
        process.terminate()
        process.join()

    # Retrieve the result if the process completed successfully
    if not result_queue.empty():
        result = result_queue.get()
        print(result)
    else:
        print("No result returned (process may have been terminated).")
