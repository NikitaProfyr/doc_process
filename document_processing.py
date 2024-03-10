import asyncio
import datetime
import json
from db_settings import get_db
from services import (
    get_data_table_query,
    execute_query,
    add_filter_in_query,
    update_query,
)


async def run_document_processing() -> bool:
    connect = await get_db()
    data_query = get_data_table_query("documents", fields=None)
    filter_query = "document_type = 'transfer_document' AND processed_at IS NULL ORDER BY recieved_at ASC"
    data_query = add_filter_in_query(data_query, filter_query=filter_query, limit=1)

    # Выборка лишь одного, самого старого по recieved_at, необработанного документа
    data = await execute_query(connect=connect, sql_query=data_query, fetching=True)

    counter_modified_objects = 0

    document_data = json.loads(data[0]["document_data"])
    operation_details = document_data.get("operation_details")
    try:
        # Обработка каждого объекта из поля document_data.objects
        for obj in document_data.get("objects"):
            filter_query = f"object = '{obj}'"
            current_object_query = get_data_table_query("data", fields=None)
            current_object_query_filter = add_filter_in_query(
                sql_query=current_object_query, filter_query=filter_query, limit=1
            )
            obj_data = await execute_query(
                connect=connect, sql_query=current_object_query_filter, fetching=True
            )

            for operation_detail, value in operation_details.items():
                if obj_data[0].get(operation_detail) == value.get("old"):

                    # Если поле в бд подходит под условие operation_details, то обновляем его
                    filter_query = "object = " + f"'{obj_data[0].get('object')}'"
                    query = update_query(
                        "data", {f"{operation_detail}": value.get("new")}
                    )
                    query = add_filter_in_query(
                        sql_query=query, filter_query=filter_query, limit=None
                    )
                    await execute_query(
                        connect=connect, sql_query=query, fetching=False
                    )
                    counter_modified_objects += 1

        execution_time = datetime.datetime.now()
        filter_query = "doc_id = " + f"'{data[0].get('doc_id')}'"
        query = update_query("documents", {"processed_at": execution_time})
        query = add_filter_in_query(query, filter_query=filter_query, limit=None)

        # Запись даты и времени обработки документа
        await execute_query(connect=connect, sql_query=query, fetching=False)

        print(f"Кол-во изменённых объектов из таблицы data {counter_modified_objects}")
        print(f"Документ {data[0].get('doc_id')} был изменён {execution_time}")
        return True
    except Exception:
        return False


asyncio.run(run_document_processing())
