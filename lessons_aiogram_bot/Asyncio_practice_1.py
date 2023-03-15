import asyncio

async def n_sec():
    n = 0
    while True:
        await asyncio.sleep(1)
        n += 1
        print(f'Прошло {n} секунд')

async def three_sec():
    while True:
        await asyncio.sleep(3) 
        print('Прошло три секунды')

async def main() -> None:
    task_1 = asyncio.create_task(n_sec())
    task_2 = asyncio.create_task(three_sec())

    await task_1
    await task_2

if __name__ == '__main__':
    asyncio.run(main())

