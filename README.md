# X Daily Top Posts

Скрипт для анализа самых популярных постов в Twitter (X) за последние 24 часа (или любой другой период) у заданных аккаунтов.

## Описание

Этот инструмент использует **X API v2** для:
- Получения идентификаторов пользователей по username
- Загрузки твитов за указанный период (по умолчанию — последние 24 часа)
- Расчета метрики вовлеченности (engagement = likes + retweets + replies + views)
- Вывода результатов в виде красивой таблицы с ранжированием
- Экспорта данных в JSON формат

## Требования

- Python 3.7+
- Аккаунт X Developer с доступом к API v2 (минимум уровень **Basic**, рекомендуется **Enterprise** для полного доступа к метрикам `public_metrics`)
- Токен доступа (Bearer Token)

## Установка зависимостей

```bash
pip install requests rich
```

## Настройка

Установите переменную окружения с вашим Bearer Token:

### Linux/macOS
```bash
export X_BEARER_TOKEN="your_bearer_token_here"
```

### Windows (PowerShell)
```powershell
$env:X_BEARER_TOKEN="your_bearer_token_here"
```

### Windows (CMD)
```cmd
set X_BEARER_TOKEN=your_bearer_token_here
```

> ⚠️ **Важно:** Для корректной работы скрипта ваш тарифный план X API должен поддерживать эндпоинты:
> - `/2/users/by/username/:username`
> - `/2/users/:id/tweets`
> - Доступ к полю `public_metrics` (включая `view_count`)

## Использование

### Базовый запуск (последние 24 часа)
```bash
python x_daily_top_posts.py
```

### Указать количество дней
```bash
python x_daily_top_posts.py --days 3
```

### Экспорт результатов в JSON
```bash
python x_daily_top_posts.py --days 1 --export results.json
```

### Комбинированный запуск
```bash
python x_daily_top_posts.py --days 7 --export weekly_top.json
```

## Аргументы командной строки

| Аргумент | Описание | По умолчанию |
|----------|----------|--------------|
| `--days` | Количество дней для анализа (период от текущей даты назад) | `1` |
| `--export` | Путь к файлу для экспорта результатов в формате JSON | Не используется |
| `--help` | Показать справку и выйти | - |

## Отслеживаемые аккаунты

По умолчанию скрипт анализирует следующие аккауны в сфере AI/ML:

- `LG_AI_Research`
- `bridgemindai`
- `MiniMax_AI`
- `OpenRouter`
- `steipete`
- `simile_ai`
- `berkeley_ai`
- `blackboxai`
- `UnslothAI`
- `openclaw`
- `Zread_ai`

Для изменения списка отредактируйте переменную `USERNAMES` в файле `x_daily_top_posts.py`.

## Формат вывода

### Таблица в терминале

```
┏━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rank ┃ Account         ┃ Post Text                                        ┃ Engagement  ┃ Link                                             ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1   │ UnslothAI       │ We just released Unsloth 2.0! Now 2x faster...   │   15,432    │ https://x.com/UnslothAI/status/1234567890      │
│  2   │ LG_AI_Research  │ Introducing our new multimodal model...          │   12,890    │ https://x.com/LG_AI_Research/status/0987654321   │
│  3   │ berkeley_ai     │ New paper: Advances in Reinforcement Learning... │    8,543    │ https://x.com/berkeley_ai/status/1122334455      │
└──────┴─────────────────┴──────────────────────────────────────────────────┴─────────────┴──────────────────────────────────────────────────┘
```

### JSON экспорт

```json
[
  {
    "rank": 1,
    "account": "UnslothAI",
    "text": "We just released Unsloth 2.0! Now 2x faster...",
    "engagement": 15432,
    "likes": 10000,
    "retweets": 3000,
    "replies": 432,
    "views": 2000,
    "url": "https://x.com/UnslothAI/status/1234567890",
    "created_at": "2024-01-15T10:30:00.000Z"
  }
]
```

## Обработка ошибок

Скрипт включает обработку следующих ситуаций:
- ❌ Недоступность X API (сетевые ошибки, таймауты)
- ❌ Ошибки аутентификации (неверный токен)
- ❌ Превышение лимитов API (Rate Limiting)
- ❌ Отсутствие твитов за указанный период
- ❌ Недоступные аккаунты (удалены, заблокированы)

При возникновении ошибок скрипт выводит подробное сообщение и продолжает обработку остальных аккаунтов.

## Лицензия

MIT License

## Вклад в проект

Не стесняйтесь создавать Issues и Pull Requests для улучшения функционала!

---

**Автор:** AI Assistant  
**Дата создания:** 2024
