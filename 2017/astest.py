'''
Just playing w/ asyncio
'''
import asyncio


queue1 = asyncio.queues.Queue()
queue2 = asyncio.queues.Queue()


async def f1():

    for i in range(0, 10, 2):
        await queue2.put(i)
        print('F1 put {:}'.format(i))

        val = await queue1.get()

        print("F1 got {:}".format(val))

async def f2():

    for i in range(1, 10, 2):
        await queue1.put(i)

        print('F2 put {:}'.format(i))

        val = await queue2.get()

        print("F2 got {:}".format(val))


futures = [f1(), f2()]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))