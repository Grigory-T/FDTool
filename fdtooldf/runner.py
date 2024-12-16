from multiprocessing import Process, Queue
import polars as pl
from .fdtool import main
from .utils import convert_col_name_back, result_dict_to_str


def run_fdtool(df, max_time=30, max_k_level=15, cut=10):
    df = df.rename(lambda el: str(el), axis=1)
    if any(True for c in df.columns if c == ""):
        raise Exception("empty string in columns NOT allowed")
    if len(df.columns) != len(set(df.columns)):
        raise Exception("columns NOT unique")
    df = df.drop_duplicates().apply(lambda ser: ser.factorize()[0])
    map_id_colname = {str(k): v for k, v in enumerate(df.columns)}
    map_colname_id = {v: k for k, v in enumerate(df.columns)}
    df.columns = [str(el) for el in range(len(df.columns))]
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
        result_dict = convert_col_name_back(result_queue.get(), map_id_colname)
        result_str = result_dict_to_str(result_dict, map_colname_id, cut)
        return (result_str, result_dict)
    else:
        print("No result returned (process may have been terminated).")
