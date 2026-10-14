import pandas as pd

from config import (
    DATA_SOURCE,
    EXCEL_FILE
)


def get_tasks():

    if DATA_SOURCE == "excel":

        return pd.read_excel(
            EXCEL_FILE,
            sheet_name="Tasks",
            engine="openpyxl"
        )

    raise Exception(
        "Graph source not configured yet."
    )


def get_buckets():

    if DATA_SOURCE == "excel":

        return pd.read_excel(
            EXCEL_FILE,
            sheet_name="Buckets",
            engine="openpyxl")
    raise Exception(
        "Graph source not configured yet."
    )