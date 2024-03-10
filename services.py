import datetime

import asyncpg


async def insert_data_table(
    table_name: str, connect: asyncpg.Connection, fields: dict
) -> None:
    """
    table_name: Название таблицы в БД
    connect: Экземпляр класса подключения к БД asyncpg
    fields: Словарь с полями и значениями, которые нужно записать в БД
    """
    columns = ", ".join(fields.keys())
    columns_value = ", ".join(
        [
            f"'{val}'"
            if isinstance(val, str) or isinstance(val, datetime.datetime)
            else str(val)
            if val is not None
            else "NULL"
            for val in fields.values()
        ]
    )

    sql_query = f"INSERT INTO public.{table_name} ({columns}) VALUES ({columns_value});"
    await connect.execute(sql_query)


def get_data_table_query(table_name: str, fields: list | None) -> str:
    """
    table_name: Наименование таблицы,
    fields: Поля в виде словаря либо None, которые нужно выбрать из бд
    """
    sql_query = "SELECT"
    if fields is None:
        sql_query += " * FROM " + "public." + table_name
    else:
        sql_query += ", ".join(fields) + " FROM " + "public." + table_name

    return sql_query


def update_query(table_name: str, fields: dict) -> str:
    """
    table_name: Наименование таблицы,
    fields: Поля в виде словаря, которые нужно обновить в записи
    ВАЖНО: после формирования данного запроса нужно добавить условие WHERE при помощи функции add_filter_in_query()
    """
    sql_query = (
        "UPDATE "
        + "public."
        + table_name
        + " SET "
        + ", ".join(
            [
                f"{key} = {value}"
                if isinstance(value, (int, float))
                else f"{key} = '{value}'"
                for key, value in fields.items()
            ]
        )
    )
    return sql_query


def add_filter_in_query(sql_query: str, filter_query: str, limit: int | None) -> str:
    """
    sql_query: Запрос к которому нужно добавить фильтрацию,
    filter_query: Параметры фильтрации для запроса
    limit: Ограничение для выборки данных
    """
    if limit is None:
        sql_query = sql_query + " WHERE " + filter_query
    else:
        sql_query = sql_query + " WHERE " + filter_query + " LIMIT " + f"{limit}"
    return sql_query


async def execute_query(
    connect: asyncpg.Connection, sql_query: str, fetching: bool
) -> list | None:
    """
    connect: Экземпляр класса подключения к БД asyncpg
    sql_query: Запрос который нужно выполнить
    fetching: True - получить данные из бд, False - какое-либо действие с данными(добавление, обновление, удаление)
    """
    query = sql_query + ";"
    if fetching:
        data = await connect.fetch(query=query)
        return data
    await connect.execute(query=query)


def get_fields_documents_tbl(item: dict) -> dict:
    fields = {
        "doc_id": item["doc_id"],
        "recieved_at ": item["recieved_at"],
        "document_type": item["document_type"],
        "document_data": item["document_data"],
        "processed_at": None,
    }
    return fields
