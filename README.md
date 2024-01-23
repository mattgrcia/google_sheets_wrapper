# Google Sheets API Python Wrapper for Dashboard Creation

This code allows you to connect a Postgres or MySQL database to a Google Sheet, designed originally for use in the creation of customized dashboards to display near real-time data to end users.

### Requirements
Along with the necessary Python packages in `requirements.txt`, you will need to have a `credentials.json` file, which is generated after creating a project on Google Cloud. This link should prove useful:

[Google Sheets API Python Quickstart Guide](https://developers.google.com/sheets/api/quickstart/python) 

Upon connecting via API for the first time, you will need to provide authorization, which will automatically generate the necessary `token.json` file in your current directory.

### Getting Spreadsheet IDs

There are two IDs of which you should take note in order to use the `insert_multiple` method effectively.

All Google Sheets have a URL structure that looks something like:

https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=GID,

where SPREADSHEET_ID is the ID for the entire Sheet (all tabs) and GID is the ID of each specific tab (usually 0 for the "first" tab).
