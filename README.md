# test_task_doc_process

## Подготовка: 

- После клонирования репозитория [создайте и активируйте виртуальное окружение](https://timeweb.cloud/tutorials/python/kak-sozdat-virtualnoe-okruzhenie#shag-1--zapuskaem-venv) в директории 
- Установите зависимости командой pip install -r requirements.txt
- Создайте файл .env и скопируйте в него данные из .env.template
- Измените переменные окружение в файле .env на нужные, для работы скрипта на вашем устройстве 
- Создайте таблицы в postgres следующими командами:
```
CREATE TABLE IF NOT EXISTS public.data
(
    object character varying(50) COLLATE pg_catalog."default" NOT NULL,
    status integer,
    level integer,
    parent character varying COLLATE pg_catalog."default",
    owner character varying(14) COLLATE pg_catalog."default",
    CONSTRAINT data_pkey PRIMARY KEY (object)
)
```
```
CREATE TABLE IF NOT EXISTS public.documents
(
    doc_id character varying COLLATE pg_catalog."default" NOT NULL,
    recieved_at timestamp without time zone,
    document_type character varying COLLATE pg_catalog."default",
    document_data jsonb,
    processed_at timestamp without time zone,
    CONSTRAINT documents_pkey PRIMARY KEY (doc_id)
)
```
- Запустите скрипт data_filler.py для генерации тестовых данных и записи их в бд
- Запустите скрипт document_processing.py для обработки записей в бд

_P.s. Специально для "Честный знак" :)_ 
