from celery import Celery
from inspect import isawaitable
import asyncio

# Celery doesn't support asyncio natively, so we have resort to a wrapper around it to enable calling `async def` functions within tasks
# taken from: https://stackoverflow.com/a/69585025/9133569
# read on why Celery struggles with supporting asyncio:
# https://github.com/celery/celery/issues/7874

class AsyncCelery(Celery):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patch_task()

    def patch_task(self):
        TaskBase = self.Task

        class ContextTask(TaskBase):
            abstract = True

            async def _run(self, *args, **kwargs):
                try:
                    result = TaskBase.__call__(self, *args, **kwargs)
                    if isawaitable(result):
                        await result
                except Exception as e:
                    # Log the error or handle it as needed
                    print(f"Task failed: {e}")
                    raise

            def __call__(self, *args, **kwargs):
                asyncio.run(self._run(*args, **kwargs))

        self.Task = ContextTask
