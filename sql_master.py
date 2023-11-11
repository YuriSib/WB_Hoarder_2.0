import sqlite3 as sq


def create_db():
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()

        cur.execute("""DROP TABLE IF EXISTS wb_table""")
        cur.execute("""DROP TABLE IF EXISTS suitable_products_table""")

        cur.execute("""CREATE TABLE IF NOT EXISTS wb_table (
            wb_id INTEGER UNIQUE,
            name TEXT,
            photo TEXT,
            price INTEGER,
            average_price INTEGER
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS suitable_products_table (
            wb_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            current_wb_price INTEGER,
            last_wb_price INTEGER,
            average_price INTEGER,
            FOREIGN KEY (wb_id) REFERENCES wb_table(wb_id)
                        )""")


def save_price_wb_table(price, wb_id):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            UPDATE wb_table
            SET price = {price}
            WHERE wb_id = {wb_id};
        """
        cur.execute(sql_query)
        con.commit()


def save_price_suitable_products_table(current_price, last_price, wb_id):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            UPDATE suitable_products_table
            SET current_wb_price = '{current_price}', last_wb_price = '{last_price}'
            WHERE wb_id = '{wb_id}';
        """
        cur.execute(sql_query)
        con.commit()


def save_in_search_table(wb_id, name, price):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            INSERT OR REPLACE INTO search_table (wb_id, name, price)
            VALUES('{wb_id}', '{name}', '{price}')
        """
        cur.execute(sql_query)
        con.commit()


def save_in_wb_table(wb_id, name, photo, price, average_price):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            INSERT OR REPLACE INTO wb_table (wb_id, name, photo, price, average_price)
            VALUES('{wb_id}', '{name}', '{photo}', '{price}', '{average_price}')
        """
        cur.execute(sql_query)
        con.commit()


def save_in_suitable_products_table(wb_id, name, current_wb_price, average_price):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query_insert = f"""
            INSERT OR REPLACE INTO suitable_products_table (wb_id, name, current_wb_price, average_price)
            VALUES('{wb_id}', '{name}', '{current_wb_price}', '{average_price}')
        """

        cur.execute(sql_query_insert)
        con.commit()


def save_average_price(wb_id, price):
    price = int(price)
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query_insert = f"""
            UPDATE wb_table
            SET average_price = '{price}'
            WHERE wb_id = '{wb_id}';
        """

        cur.execute(sql_query_insert)
        con.commit()


def check_id(wb_id, table):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT wb_id
            FROM {table}
            WHERE wb_id = {wb_id};
        """

        cur.execute(sql_query)
        check = True if cur.fetchone() else False

    return check


def load_row_for_id(wb_id, table):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT *
            FROM {table}
            WHERE wb_id = {wb_id};
        """

        cur.execute(sql_query)
        row = cur.fetchone()

    return row


def load_rows_from_suitable_products_table():
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT *
            FROM 'suitable_products_table'
        """

        cur.execute(sql_query)
        row = cur.fetchall()

    return row


def load_property_and_price(category):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT *
            FROM 'property_and_price'
            WHERE name = '{category}'
        """

        cur.execute(sql_query)
        row = cur.fetchall()

    return row


def qwery_from_sql(wb_id):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT name
            FROM wb_table
            WHERE wb_id = {wb_id};
        """
        cur.execute(sql_query)
        row = cur.fetchone()
        qwery = ''.join(row)

    return qwery


def sql_row_counter(table):
    with sq.connect('hoarder.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT COUNT(*) FROM {table};
        """
        cur.execute(sql_query)
        quantity_rows = cur.fetchone()

        return quantity_rows


if __name__ == "__main__":
    # save_in_sql(160433652, 'name', 100500, 0)

    # result = load_row_for_id(160433652, 'wb_table')
    # print(result)

    # a = qwery_in_sql(160433652)
    # print(a)
    # save_price_in_sql(66613, 160433652)
    create_db()
    # print(load_rows_from_suitable_products_table())
    # print(load_row_for_id(70730317, 'wb_table'))

