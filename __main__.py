#!./interpreter/bin/python
from pathlib import Path

from time_lapse_worker import TimeLapseWorker


if __name__ == "__main__":

    target_folder = Path(__file__).parent / "140521"
    time_lapse_worker = TimeLapseWorker(60*5, target_folder, 1000)
    time_lapse_worker.start()
