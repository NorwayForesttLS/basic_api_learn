import time
from main import main

while True:
    try:
        main()
        print("Анализ завершён. Следующий запуск через 1 час...")

        time.sleep(3600)
    except Exception as e:
        print(f"Что то пошло не так {e}")
        time.sleep(60)

