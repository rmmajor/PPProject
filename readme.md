# Представляємо вам маркетплейс квитків на різноманітні заходи: концерти, театральні вистави, лекції, зустрічі тощо.

---

## Встановити проєкт

    Клонувати з гіта
    Найкраще запустити зразу з Pycharm і вибрати в налаштуваннях інтерпретатора pipenv
    Варто перевірити, чи вибрано посилання на еxe файл
    
## Для pipenv
    pipenv install
    pipenv local <версія пайтона>
    pipenv update 
    pipenv shell

## SQLALCHEMY/ALEMBIC команди для створення бази//
    alembic revision --autogenerate -m "Create models"   
    alembic upgrade head

## Запуск сервера
    waitress-serve main:app
