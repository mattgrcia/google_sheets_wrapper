import pandas as pd
from google_sheets import Connector as GoogleSheetsConnector
from postgres import Connector as PGConnector


class Updater(GoogleSheetsConnector, PGConnector):
    def __init__(self):
        super().__init__()
        self.spreadsheet_id = "SPREADSHEET_ID"

    def pull_from_db(self):
        query = """
                QUERY_TO_GET_DATA
                """
        self.cur.execute(query)

        df = pd.DataFrame(self.cur.fetchall(), columns=["COLUMNS HERE"])

        df.fillna("", inplace=True)

        type_dict = {
            "FIELD": "FIELD_TYPE, e.g. float, int, str",
            "FIELD": "FIELD_TYPE",
            "FIELD": "FIELD_TYPE",
            "FIELD": "FIELD_TYPE",
        }

        # fill NAs correctly, depending on field type
        na_dict = {}
        for c in df.columns:
            if type_dict.get(c) in ["float", "int"]:
                na_dict[c] = "0"
            else:
                na_dict[c] = ""

        df.fillna(na_dict, inplace=True)
        df = df.astype(type_dict)

        return df

    def push_to_db(self):
        # get values from the Google Sheet
        result = (
            self.sheet.values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range="Tab Name!Range, e.g. A1:N10000",
            )
            .execute()
        )
        values = result.get("values", [])

        # create a pandas DataFrame from the values
        df = pd.DataFrame(values)
        headers = df.iloc[0]
        df = pd.DataFrame(df.values[1:], columns=headers)

        df = df[
            [
                "FIELD NAMES",
            ]
        ]

        # DO SOMETHING WITH THE DATA HERE, e.g. update the database

        return None

    def refresh(self):
        # update the database with values currently on the Google Sheet
        self.push_to_db()

        # get data from the database
        data = self.pull_from_db()

        # refresh the Google Sheet to display updated data
        tabs = {
            "Active Users": {
                "spreadsheet_id": self.spreadsheet_id,
                "gid": 0,  # GID of specific Sheet tab (number at end of URL)
                "function": data,
                "start_clear": "CELL FROM WHICH YOU WANT TO START CLEARING DATA",
                "end_clear": "CELL TO WHICH YOU WANT TO CLEAR DATA",
                "start_cell": "CELL FROM WHICH YOU WANT TO START INSERTING DATA, e.g. A2",
                "end_cell": "CELL TO WHICH YOU WANT TO INSERT DATA, e.g. E2",
                # optional date cells can be added to insert date and time of updates
                # "date_cell": "A5",
                # "time_cell": "B5",
            },
        }

        self.insert_multiple(tabs)

        return None
