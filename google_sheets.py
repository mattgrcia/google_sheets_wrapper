import datetime
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import pandas as pd


class Connector:
    def __init__(self):
        super().__init__()
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        try:
            self.credentials = Credentials.from_authorized_user_file(
                "token.json", self.SCOPES
            )

        except Exception as e:
            print(f"Error: {e}")
            self.get_new_token()
            time.sleep(30)
            self.credentials = Credentials.from_authorized_user_file(
                "token.json", self.SCOPES
            )

        self.service = build("sheets", "v4", credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def get_spreadsheet_values(self, spreadsheet_id, tab_name, start_cell, end_cell):
        result = (
            self.sheet.values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=f"{tab_name}!{start_cell}:{end_cell}",
            )
            .execute()
        )
        values = result.get("values", [])

        return values

    @staticmethod
    def spreadsheet_values_to_df(values, header_row=0, offset=1):
        df = pd.DataFrame(values)
        headers = df.iloc[header_row]
        df = pd.DataFrame(df.values[header_row + offset :], columns=headers)
        df = df.replace("", "0").fillna("0")

        return df

    def clear_values(self, spreadsheet_id, ranges):
        batch_clear_values_request_body = {
            # The ranges to clear, in A1 notation.
            "ranges": ranges,
        }

        request = (
            self.service.spreadsheets()
            .values()
            .batchClear(
                spreadsheetId=spreadsheet_id, body=batch_clear_values_request_body
            )
        )
        request.execute()

        return None

    def delete_rows(self, spreadsheet_id, tab_id, start_index, end_index):
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": tab_id,
                            "dimension": "ROWS",
                            "startIndex": start_index,
                            "endIndex": end_index,
                        }
                    }
                }
            ],
        }

        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body
        )
        request.execute()

        return None

    def get_new_token(self):
        # os.remove('token.json')
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", self.SCOPES
        )
        self.credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(self.credentials.to_json())

        return None

    def insert_values(self, spreadsheet_id, value_range, values_to_insert):
        value_input_option = "RAW"
        insert_data_option = "INSERT_ROWS"

        value_range_body = {
            "range": value_range,
            "majorDimension": "ROWS",
            "values": values_to_insert,
        }

        request = (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=value_range,
                valueInputOption=value_input_option,
                insertDataOption=insert_data_option,
                body=value_range_body,
            )
        )
        request.execute()

        return None

    def insert_multiple(self, tabs):
        date_list = [[datetime.datetime.now().strftime("%Y-%m-%d")]]
        time_list = [[datetime.datetime.now().strftime("%H:%M:%S")]]

        for k, v in tabs.items():
            try:
                self.delete_rows(
                    v["spreadsheet_id"], v["gid"], v["start_delete"], v["end_delete"]
                )
            except Exception:
                print(f"Error deleting rows. Moving forward...")

            self.clear_values(
                v["spreadsheet_id"], f'{k}!{v["start_clear"]}:{v["end_clear"]}'
            )
            self.insert_values(
                v["spreadsheet_id"],
                f'{k}!{v["start_cell"]}:{v["end_cell"]}',
                v["function"],
            )

            if "date_cell" in v:
                self.update_values(
                    v["spreadsheet_id"], f'{k}!{v["date_cell"]}', date_list
                )
                self.update_values(
                    v["spreadsheet_id"],
                    f'{k}!{v["time_cell"]}',
                    time_list,
                    "USER_ENTERED",
                )

            print(f"Updated {k}!")

        return None

    def update_values(
        self, spreadsheet_id, value_range, values_to_insert, value_input_option="RAW"
    ):
        value_range_body = {
            "range": value_range,
            "majorDimension": "COLUMNS",
            "values": values_to_insert,
        }

        request = (
            self.service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=value_range,
                valueInputOption=value_input_option,
                body=value_range_body,
            )
        )
        request.execute()

        return None
