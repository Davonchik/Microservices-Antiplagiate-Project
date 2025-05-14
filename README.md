# Общий отчёт об итогах проекта (КР2)

# Выполнил студент 2 курса ФКН ПИ, Асланян Давид, группы БПИ236

## Как запустить проект

Находясь в корневом каталоге проекта, нужно вписать в терминал команду поднятия docker-контейнеров:

```
docker compose up --build
```

После запуска - переходите в postman и можно протестировать работу проекта.

## 1. Краткое соответствие критериям

- **Функциональность (2 балла)**  
  - FileStoringService: загрузка `.txt`, дедупликация SHA-256 (проверка на антиплагиат 100%), стриминг файла пользователю  
  - FileAnalysisService: подсчёт абзацев, слов и символов; опциональная генерация облака слов  

- **Микросервисность (4 балла)**  
  - Два независимых микросервиса (FileStoringService и FileAnalysisService)  
  - Единая точка входа через Nginx API Gateway  
  - Отдельные базы PostgreSQL на портах 5432 и 5433  
  - Корректная обработка ошибок (404, 409, 422, 503, 500)  

- **Swagger / Postman (1 балл)**  
  - Автогенерируемая документация Swagger UI на `/docs` для каждого сервиса  
  - Экспорт коллекции Postman в папке `postman/`  

- **Качество кода и документация (2 балла)**  
  - Чистая архитектура (Domain, Use Cases, Infrastructure, Presentation)  
  - Подробные README-файлы и этот общий отчёт в Markdown  

- **Тесты и покрытие ≥ 65 % (1 балл)**  
  - Unit-тесты для бизнес-логики  
  - Общий охват кода ~ 85 % в каждом сервисе  

---

## 2. Роль API Gateway (Nginx)

API Gateway на Nginx маршрутизирует запросы от клиентов к микросервисам:

```nginx
http {
    upstream file_storing_service {
        server file_storing_service:8000;
    }
    upstream file_analisys_service {
        server file_analisys_service:8001;
    }

    server {
        listen 80;
        
        location /file_storing_service/ {
            proxy_pass http://file_storing_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        location /file_analisys_service/ {
            proxy_pass http://file_analisys_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

events {}
```

