import asyncio

# результатом вывода асинхронной функции является объект корутина

async def send_hello():
    # await - значит контроль кода переходит другому блоку, а этот пока ждет
    # в этот момент времени может запускаться и работать другая функция
    await asyncio.sleep(2) # испольнение кода начинается через две секунды
    print('hi')
    # как проходит две секунды, контроль исполнения кода возвращается к функции и она исполняется дальше
async def send_bye():
    await asyncio.sleep(1)
    print('bye')

async def main():
    # объявляем (регистрируем) объекты корутины как задачи конкурентного исполнения кода
    task_1 = asyncio.create_task(send_hello())
    task_2 = asyncio.create_task(send_bye())

    await task_1
    await task_2

asyncio.run(main())

# просто вызвать функцию print(send_hello) нельзя
# реализовывать вывод функции нужно через метод run
#asyncio.run(send_hello())
# функция run - не асинхронная и выполняется по порядку