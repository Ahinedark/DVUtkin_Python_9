"""Домашнее задание к лекции 5 "ООП". Уткин Д.В.

Работе с файлами Вас обучили на прошлых заданиях (библиотека `os`).  
Создать программу, которая по заданному адресу (`URL = 'https://loremflickr.com/1280/720/kittens'`) скачает 5 файлов в локальную директорию(папку/каталог) на Вашем компьютере(ноутбуке). 
Требуется реализовать программу не только в *асинхронном варианте*, но и в *синхронном варианте*, чтобы можно было сравнить время выполнения.<br>
<br>
Вам потребуется (из того, что не проходили на прошлых лекциях):
- для синхронного варианта:
  - библиотека requests (получение контента файла `cont = requests.get(URL)`, )
- для асинхронного варианта:
    - библиотека aiohttp (работа с сессией `aiohttp.ClientSession()` и получение контента файла `session.get(URL)`, )
    - библиотека для асинхронной работы с файлами **aiofiles**<br>
вместо<br>
`with open(filename`<br>
использовать<br>
`async with aiofiles.open(filename`
"""

import asyncio
import os
import random
import time

import aiofiles
import aiohttp
import requests

URL_BASE = 'https://placebear.com'
SAVE_PATH = 'downloads'


def url_constructor() -> str:
    """Генерации url для получения картинки с placebear.

    Returns:
        str: строка url вида: "https://placebear.com/{width}/{height}".
    """
    width = random.randint(400, 800)
    height = random.randint(400, 800)
    url = f'{URL_BASE}/{width}/{height}'
    return url


def func_sync():
    """Скачивание 5 картинок в синхронном режиме."""
    print('Выполняется синхронная функция:')
    start_total = time.time()

    for i in range(1, 6):
        url = url_constructor()
        start = time.time()

        # Получаем контент ответа
        cont = requests.get(url).content  # noqa: S113

        # Сохраняем картинку
        f_name = f'sync_mendvedn_{i}.jpg'
        f_path = os.path.join(SAVE_PATH, f_name)  # noqa: PTH118
        with open(f_path, 'wb') as f:  # noqa: PTH123
            f.write(cont)

        end = time.time()
        print(f'\tФайл {f_name} сохранён за {end - start} секунд.') 

    end_total = time.time()
    print(f'Синхронная функция выполнена за {end_total - start_total} секунд.') 


async def download_image(session:aiohttp.ClientSession, i):
    """Скачивание 1 картинки в синхронном режиме.

    Args:
        session (aiohttp.ClientSession): Сессия.
        i (_type_): Индекс картинки (для сохранения).
    """
    url = url_constructor()
    start = time.time()

    # Получаем контент ответа
    async with session.get(url) as resp:
        cont = await resp.read()
    
    # Сохраняем картинку
    f_name = f'async_mendvedn_{i}.jpg'
    f_path = os.path.join(SAVE_PATH, f_name)  # noqa: PTH118
    async with aiofiles.open(f_path, 'wb') as f:
        await f.write(cont)    

    end = time.time()
    print(f'\tФайл {f_name} сохранён за {end - start} секунд.') 


async def func_async():
    """Скачивание картинок в синхронном режиме."""
    print('Выполняется асинхронная функция:')
    start_total = time.time()

    # Запускаем асинхронно 5 загрузок в 1 сессии
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image(session, i)
            for i in range(1, 6)
        ]
        await asyncio.gather(*tasks)

    end_total = time.time()
    print(f'Асинхронная функция выполнена за {end_total - start_total} секунд.') 


def main():
    """Главная функция.

    Создаёт папку для сохранения изображений.
    Запускает синхронную функцию, затем асинхронную. 
    """
    os.makedirs(SAVE_PATH, exist_ok=True)  # noqa: PTH103
    # Запускаем синхронную функцию
    func_sync()
    print('')
    # Запускаем асинхронную функцию
    asyncio.run(func_async())


if __name__ == '__main__':
    main()