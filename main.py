import json

import psycopg2

# defines the table columns and values | this is used on
# init_app to create the necessary table
column_data = {
    "I3": None,
    "IB": None,
    "AV": None,
    "BI": None,
    "AU": None,
    "BC": None,
    "CO": None,
    "ED": None,
    "IL": None,
    "EI": None,
    "IU": None,
    "CP": None,
    "LA": None,
    "MP": None,
    "NC": None,
    "PD": None,
    "PA": None,
    "NP": None,
    "RP": None,
    "RI": None,
    "RE": None,
    "DI": None,
    "PU": None,
    "YP": None,
    "RC": None,
    "RS": None,
    "SR": None,
    "SE": None,
    "TI": None,
    "ST": None,
    "PT": None,
    "TR": None,
    "PN": None,
    "DE": None,
    "EA": None,
    "RF": None,
    "RD": None,
    "SI": None,
    "WE": None,
    "SG": None,
    "PI": None,
    "GC": None,
    "TP": None,
}


def get_config() -> dict:
    """Reads the config.josn file converts to dict and returns the configuration dict."""

    with open("./config.json") as f:
        config = json.load(f)
        return config


def get_pg_cursor():
    """Connects to postgres and returns the cursor."""

    params = get_config()["db_connect"]
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    return conn.cursor()


def init_app_table():
    """
    The values read from the file are to be stored in the table.
    This function initializes the table and inserts the necessary data.
    """

    table_name = get_config()["table_name"]
    cursor = get_pg_cursor()

    def get_table_creation_command() -> str:
        """Returns a string that can be executed to create the table."""

        column_names = list(column_data.keys())
        columns_string = ""  # contains `column_name VARCHAR(255) NOT NULL, ...`
        for index in range(len(column_names)):
            columns_string += f"{column_names[index]} TEXT"
            columns_string += "," if index != len(column_names) - 1 else ""

        return f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, {columns_string})"

    # delete existing table
    try:
        cursor.execute(f"DROP TABLE {table_name}")
    except psycopg2.errors.UndefinedTable:
        # table does not exist | no problem
        pass

    # table created
    cursor.execute(get_table_creation_command())


def init_app():
    """Called for initializing the app. To check if everything is properly given."""

    init_app_table()


def join_list(input_list: list) -> str:
    """Joins a given list to a string. Used in db functions."""

    str1 = " ".join([elem for elem in input_list[1:]])
    return str1


def start():
    """Main function to start the algorithm. Called after init and stuff."""

    input_file = open("GARDBIB.TXT", "r")
    records_count = 0
    data_store = []

    for line in input_file:
        single_line_data: list = line.split()

        if line.find("**") == 0:
            if line.find("**START") == 0:
                index = 1
            else:
                index = 0
        else:
            index = -1

        if len(single_line_data) > 1:
            if column_data[single_line_data[0]] is not None:
                column_data[single_line_data[0]] += "," + join_list(single_line_data)
            else:
                column_data[single_line_data[0]] = join_list(single_line_data)

        if index == 0:
            column_data["I3"] = int(column_data["I3"])
            data_store.append(tuple(column_data.values()))
            column_data.update((k, None) for k in column_data)

        if len(data_store) == 5000:
            records_count += 5000
            print(f"Iterator: {records_count}")

            cursor = get_pg_cursor()
            column_values_string = ",".join(["%s"] * len(column_data))
            column_names_string = ",".join(column_data.keys())
            insert_statement = f"INSERT INTO %s (%s) VALUES (%s);" % (
                get_config()["table_name"],
                column_names_string,
                column_values_string,
            )
            cursor.executemany(insert_statement, data_store)
            del data_store[:]

    print(f"Total Records: {records_count}")


if __name__ == "__main__":
    init_app()
    start()
