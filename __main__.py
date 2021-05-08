#!./interpreter/bin/python
from pathlib import Path

from time_lapse_worker import TimeLapseWorker


if __name__ == "__main__":

    target_folder = Path(__file__).parent / "test_photos"
    time_lapse_worker = TimeLapseWorker(5, target_folder, 540)
    time_lapse_worker.start()
