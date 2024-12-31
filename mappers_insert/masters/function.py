import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import URL
from datetime import date, timedelta, datetime
import base64
import numpy as np

def user_create_parser(request):
    """
    Parses user creation request data.

    Args:
        request: The HTTP request object containing POST data.

    Returns:
        dict: A dictionary containing user and profile data.
    """
    params = request.POST.dict()
    userdata = {
        "first_name": params.get("first_name"),
        "last_name": params.get("last_name"),
        "username": params.get("email"),
        "email": params.get('email'),
    }
    profiledata = {
        "Role": params.get("role"),
        "CreatedID": request.user,
        "UpdatedID": request.user,
    }
    return {"user": userdata, "profile": profiledata}

def user_edit_parser(request):
    """
    Parses user edit request data.

    Args:
        request: The HTTP request object containing POST data.

    Returns:
        dict: A dictionary containing user and profile data.
    """
    params = request.POST.dict()
    userdata = {
        "first_name": params.get("first_name"),
        "last_name": params.get("last_name"),
        "username": params.get("email"),
        "email": params.get('email'),
    }
    profiledata = {
        "Role": params.get("role"),
        "UpdatedID": request.user,
    }
    return {"user": userdata, "profile": profiledata}

def format_feed_data(request):
    """
    Formats feed data from the request.

    Args:
        request: The HTTP request object containing data.

    Returns:
        dict: A dictionary containing formatted feed data.
    """
    params = request.data.dict()
    print(params, "functions")
    feed_data = {
        "Name": params.get('name', ''),
        "Description": params.get('description', ''),
        "CreatedID": request.user.id,
        "UpdatedID": request.user.id,
    }
    return feed_data

def format_feed_category_data(request):
    """
    Formats feed category data from the request.

    Args:
        request: The HTTP request object containing data.

    Returns:
        dict: A dictionary containing formatted feed category data.
    """
    params = request.data.dict()
    print(params, "functions")
    feed_data = {
        "Name": params.get('name', ''),
        "Description": params.get('description', ''),
        "CreatedID": request.user.id,
        "UpdatedID": request.user.id,
    }
    return feed_data

def ExecuteSQLQuery(SQLQuery):
    """
    Executes an SQL query and returns the result as a DataFrame.

    Args:
        SQLQuery (str): The SQL query to execute.

    Returns:
        DataFrame: The result of the SQL query.
    """
    print(str(base64.b64decode("MzBBOHIweUpiZnMqZUh0bCNmRCU="), "utf-8"))
    sql_conn_url = URL.create(
        drivername="mssql+pyodbc",
        username="x_TpdePythonJobs",
        password="isz0Gs8G9EQqGMvtjvCM",
        host="dia1tpawsql0001",
        database="DBPREP1",
        query={
            "driver": "ODBC Driver 17 for SQL Server",
        }
    )
    db_prep_engine = create_engine(sql_conn_url)
    conn = db_prep_engine.connect()
    with db_prep_engine.connect() as conn:
        data = pd.read_sql(
            sql=SQLQuery,
            con=conn.connection
        )
    db_prep_engine.dispose()
    return data

class SQLCONNECTION:
    """
    A class to handle SQL connections.
    """
    def __init__():
        """
        Initializes the SQLCONNECTION class.
        """
        pass

class Validation:
    """
    A class to handle various validation checks on data.
    """
    def __init__(self):
        """
        Initializes the Validation class.
        """
        pass

    @staticmethod
    def CheckBlankColumns(row, NonBlankColumns):
        """
        Checks for blank columns in a row.

        Args:
            row (Series): The row to check.
            NonBlankColumns (list): List of columns that should not be blank.

        Returns:
            list: List of columns that are blank.
        """
        print("\nrow: ", row)
        null_columns = [col for col in NonBlankColumns if (pd.isnull(row[col]) or pd.isna(row[col]))]
        print("\nnull_columns", null_columns)
        if null_columns:
            return null_columns
        else:
            return ''

    @staticmethod
    def check_duplicate_rows(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Checks for duplicate rows in a DataFrame.

        Args:
            df (DataFrame): The DataFrame to check.
            columns (list): List of columns to check for duplicates.

        Returns:
            DataFrame: The DataFrame with a new column indicating duplicate entries.
        """
        print("Entering inside the function")
        s = df[columns].duplicated()
        df = pd.concat([df, s.rename("duplicated_entry_bool")], axis=1)
        df['DuplicateEntry'] = df["duplicated_entry_bool"].apply(
            lambda x: True if x else False)
        df = df.drop(['duplicated_entry_bool'], axis=1)
        print("Returning the final dataframe")
        return df

    @staticmethod
    def check_values_range(df, column_name='', new_column_name='', values_range=[], present='', not_present=''):
        """
        Checks if values in a column are within a specified range.

        Args:
            df (DataFrame): The DataFrame to check.
            column_name (str): The column to check.
            new_column_name (str): The name of the new column to store the check results.
            values_range (list): The range of acceptable values.
            present (str): The value to assign if the value is within the range.
            not_present (str): The value to assign if the value is not within the range.

        Returns:
            DataFrame: The DataFrame with a new column indicating the check results.
        """
        new_column_name = new_column_name if new_column_name else 'check ->{}'.format(column_name)
        Mapping['Check -> UploadValuations'] = Mapping['UploadValuations'].apply(lambda x: 'Please Enter 0/1 for UploadValuations' if x not in [0, 1] else '')
        df[new_column_name] = df[column_name].apply(
            lambda x: not_present if x not in values_range else present)
        return df

    @staticmethod
    def trimspaces(df, columns):
        """
        Removes whitespace from all columns in a DataFrame.

        Args:
            df (DataFrame): The DataFrame to process.
            columns (list): List of columns to trim whitespace from.

        Returns:
            DataFrame: The DataFrame with whitespace removed from specified columns.
        """
        for Column in columns:
            df[Column] = df[Column].apply(lambda x: x.strip() if isinstance(x, str) else x)
        return df

    @staticmethod
    def error_bool(row, checkcolumns):
        """
        Checks if there are any errors in specified columns of a row.

        Args:
            row (Series): The row to check.
            checkcolumns (list): List of columns to check for errors.

        Returns:
            bool: True if there are errors, False otherwise.
        """
        for col in checkcolumns:
            if row[col]:
                return True
        return False

    @staticmethod
    def error_dict(row, checkcolumns):
        """
        Creates a dictionary of errors for specified columns in a row.

        Args:
            row (Series): The row to check.
            checkcolumns (list): List of columns to check for errors.

        Returns:
            dict: A dictionary of errors.
        """
        error_columns = {}
        for col in checkcolumns:
            if col == 'Check -> BlankColumns':
                if row[col]:
                    for key in row[col]:
                        error_columns.update({key: f'{key} cannot be blank'})
            else:
                if row[col]:
                    error_columns.update({str(col.split('->')[1]).strip(): row[col]})
        return error_columns