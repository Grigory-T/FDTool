from multiprocessing import Process, Queue
from .fdtool import main
import polars as pl


def run_fdtool(df, max_time=30, max_k_level=15):
    df = df.rename(lambda el: str(el), axis=1)
    if any(True for c in df.columns if c == ""):
        raise Exception("empty string in columns NOT allowed")
    if len(df.columns) != len(set(df.columns)):
        raise Exception("columns NOT unique")
    df = df.drop_duplicates().apply(lambda ser: ser.factorize()[0])
    df = pl.from_pandas(df)

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
