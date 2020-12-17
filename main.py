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
    cur = conn.cursor()
    return cur


def init_app_table():
    """
    The values read from the file are to be stored in the table.
    This function initializes the table and inserts the necessary data.
    """

    table_name = get_config()["table_name"]

    table_creation_columns_string = (
        ""  # contains `column_name VARCHAR(255) NOT NULL, ...`
    )
    for column in column_data.keys():
        table_creation_columns_string += f"{column} VARCHAR(255) NOT NULL,"

    table_creation_command = f"""
        CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                {table_creation_columns_string}
        )
    """

    cursor = get_pg_cursor()
    cursor.execute(f"DROP TABLE {get_config()}")
    cursor.execute(table_creation_command)


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
