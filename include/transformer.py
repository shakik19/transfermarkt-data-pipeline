import os
import logging
import threading
import pandas as pd
from pyarrow import csv, parquet as pq


class DataTransformer:
    def __init__(self, project_name: str):
        self.DATASET_DIR = os.environ.get("DATASET_DIR")
        self.PROJECT_DATASET_DIR = os.path.join(self.DATASET_DIR, project_name)
        self.CSV_DATASET_DIR = os.path.join(self.PROJECT_DATASET_DIR, "csv")
        self.PARQUET_DATASET_DIR = os.path.join(self.PROJECT_DATASET_DIR, "parquet")
        self.TABLES = ["game_lineups", "appearances", 
                       "game_events", "games",
                       "players", "player_valuations",
                       "club_games", "clubs"]
        self.logger = logging.getLogger(__name__)


    def exclude_corrupt_columns(self, filename: str, columns: list[str]):
        # Excluding corrupted columns in the dataset
        filename = f"{filename}.csv"
        filepath = os.path.join(self.CSV_DATASET_DIR, filename)
        df = pd.read_csv(filepath)

        if set(columns).issubset(df.columns):
            df = df.drop(columns=columns, axis=1)
            self.logger.info(f"Removed corrupted {columns} from {filename}")
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved {filename}")
        else:
            self.logger.info("No corrupt column exists")


    def process_csv_to_parquet(self, filename: str):
        csv_path = f"{self.CSV_DATASET_DIR}/{filename}.csv"
        parquet_path = f"{self.PARQUET_DATASET_DIR}/{filename}.parquet"

        arrow_table = csv.read_csv(csv_path, csv.ReadOptions(block_size=100000))
        self.logger.info(f"Parsed {filename}.csv to Arrow table")

        pq.write_table(arrow_table, parquet_path)
        self.logger.info(f"Saved {filename}.parquet to {self.PARQUET_DATASET_DIR}")


    def csv_to_parquet(self):
        threads = []
        for table in self.TABLES:
            self.logger.info("Starting task")
            thread =  threading.Thread(target=self.process_csv_to_parquet,
                                       args=[table])
            threads.append(thread)
            thread.start()
            self.logger.info(f"{table} thread started")           
        for thread in threads:
            self.logger.info(f"{table} thread joined")           
            thread.join()
    