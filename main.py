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
            columns_string += f"{column_names[index]} VARCHAR(255) NOT NULL"
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


#
# connection = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="EClavan956#",
#     db="tagsys",
#     cursorclass=pymysql.cursors.DictCursor,
# )
# print("connect successful!!!")
#
#
# def concateFunc(list1):
#     str1 = " ".join([elem for elem in list1[1:]])
#     return str1
#
#
# file1 = open("GARDBIB.TXT", "r")

# count_records = 0
# l1 = []
# # for line in islice(file1,1000):
# for line in file1:
#     line1 = line.split()
#     index1 = 0
#     if line.find("**") == 0:
#         if line.find("**START") == 0:
#             index1 = 1
#         else:
#             index1 = 0
#     else:
#         index1 = -1
#     if len(line1) > 1:
#         if column_data[line1[0]] is not None:
#             column_data[line1[0]] += "," + concateFunc(line1)
#         else:
#             column_data[line1[0]] = concateFunc(line1)
#     if index1 == 0:
#         column_data["I3"] = int(column_data["I3"])
#         l1.append(tuple(column_data.values()))
#         column_data.update((k, None) for k in column_data)
#     if len(l1) == 5000:
#         with connection.cursor() as cursor:
#             placeholders = ",".join(["%s"] * len(column_data))
#             columns = ",".join(column_data.keys())
#             sql = "INSERT INTO `mytable1` (%s) VALUES (%s)" % (columns, placeholders)
#             count_records += 5000
#             print("Iterator : ", count_records)
#             cursor.executemany(sql, l1)
#             del l1[:]
#             connection.commit()
# print("Total Records : ", count_records)

if __name__ == "__main__":
    init_app()
