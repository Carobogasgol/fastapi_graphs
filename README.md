# FastAPI Graphs

FastAPI приложение для создания, чтения и изменения направленных ациклических графов

## Предоставляемые возможности

- Создание графов
- Получение списков смежности графа (как обычных, так и транспонированных)
- Удаление вершин
- Интеграция с базой данных PostgreSQL
- Поддержка Docker для упрощения развертывания

## Запуск приложения

1. Запуск БД и приложения:
```bash
docker-compose up
```

API будет запущено на  `http://localhost:8080`

Документация:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Запуск тестов

Чтобы запустить тесты отдельно:

```bash
docker-compose up test
```

## API Endpoints

- `POST /api/graph/` - Создаёт новый граф
- `GET /api/graph/{graph_id}` - Выводит список вершин и рёбер
- `GET /api/graph/{graph_id}/adjacency_list` - Выводит граф в виде списка смежности
- `GET /api/graph/{graph_id}/reverse_adjacency_list` - Выводит транспонированный граф в виде списка смежности
- `DELETE /api/graph/{graph_id}/node/{node_name}` - Удаляет вершину и связанные с ней рёбра

## Структура проекта:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_graph_creation.py
│   └── test_node_deletion.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Схема БД

БД содержит следующие таблицы:
- `graphs` - хранит данные графа
- `vertices` - хранит вершины
- `edges` - хранит рёбра, соединяющие вершины
