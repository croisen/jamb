import functools
import typing
import asyncio


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        f = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, f)

    return wrapper
