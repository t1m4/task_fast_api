# Installation #

1. Start docker containers
    ```bash
        docker-compose -f local.yml up 
        docker-compose -f local.yml up --build # build containers again
        docker-compose -f local.yml up -d # run in background
 
   ```
2. Connect to `app` container
   ```bash
        docker-compose -f local.yml exec app /bin/bash
    ```
3. Run migrations using `alembic`
    ```bash
        alembic upgrade head
    ```
    Notice that you should have `alembic` folder with migrations.
    If you don't have it:
   1. Init alembic folder
       ```bash
      alembic init alembic
      ```
   2. And change `sqlalchemy.url` in `alembic.ini` file or configure it in `env.py`
   3. Create you first migration
      ```bash
      alembic revision --autogenerate -m "First migration"
      ```
   4. And then you can `alembic upgrade head`
4. Create initial data. Generally, it creates superuser for testing. You can configure it in 
   `task_fast_api/.env` file. 
5. Run tests using `pytest`
    ```bash
    pytest -s
   ```
# Documentation #
1. Go to `/docs/` to try all endpoint by himself.
2. Go to `/redoc/` to check Documentation for each endpoint
