# StudentAssistant
Создание ИИ-ассистента для студентов на основе RAG-архитектуры и методологии проектной деятельности

Краткое описание:

Студенты, работая над проектами, часто сталкиваются не с техническими, а с методологическими трудностями: как планировать задачи, вести документацию, распределять роли. Этот проект предлагает создать ИИ-ассистента, который станет для них "карманным" ментором. В отличие от обычных LLM, он будет давать ответы строго на основе проверенной базы знаний (статьи, книги, ГОСТы по Agile, Scrum, DevOps и т.д.).

# Состав команды:

- Соболев Егор Владимирович РИ-420950 (Аналитик/Тестировщик)
- Раков Дмитрий Владимирович РИ-420931 (Тимлид/Менеджерпроекта)
- Яцук Владислав Романович РИ-420935 (ML-разработчик)
- Косторной Дмитрий Вадимович РИ-420936 (Разработчик (Backend))

Командная видео-презентация:
https://drive.google.com/file/d/1cI9er5NTaOPD3ixKoVKL0DfPCnW6SZi-/view?usp=drive_link

Презентация:
https://docs.google.com/presentation/d/1TaUUCi4FTAWLk_CCYDL_L6UmPpI9I5Jy/edit?usp=drive_link&ouid=104831584149150055496&rtpof=true&sd=true

Видео-пример работы продукта:
https://drive.google.com/file/d/1GhaTRjbhSqFgEmS5MwldGOrc4x6DyLlt/view?usp=drive_link

# Локальный запуск
Для запуска локально необходимо:

.env файл с содержимым:

```
TELEGRAM_BOT_TOKEN=Токен вашего бота
RAG_API_URL=http://rag-api:8000
DATABASE_URL=sqlite+aiosqlite:///./data/project_assistant.db
LLM_BASE_URL=http://ollama:11434
LLM_MODEL=gemma3:4b
```

Выполнение команд:

```
docker exec project_assistant_ollama ollama pull gemma3:4b
```

```
docker-compose up --build
```

Нужно убедиться, что модель появилась в списке:

```
docker exec project_assistant_ollama ollama list
```

Если по какой-то причине сервисы "project_assistant_rag_api" и "project_assistant_bot" не запустились, можно выполнить команды:

```
docker start project_assistant_rag_api
docker start project_assistant_bot
```

Если по какой-то причине векторная база не инициализировалась автоматически, можно выполнить команду:
```
docker exec -it project_assistant_rag_api python scripts/initial_setup.py
```
