from __future__ import absolute_import
from __future__ import print_function
import asyncio
import random


from typing import Any

import httpx


from app.exceptions import TooManyRequestsException
from pydantic import BaseModel


class Session(BaseModel):
    semaphore: int = None
    max_tries: int = 5
    sem: Any = None
    client: Any = None

    async def setup(self):
        self.client = httpx.Client()
        if self.semaphore:
            self.sem = asyncio.Semaphore(self.semaphore)
        else:
            self.sem = asyncio.Semaphore(250)

    async def _request(self, method, url, **kwargs):
        tries = 0
        while tries < self.max_tries:
            print(tries)
            async with self.sem:
                try:
                    resp = None
                    status = None
                    async with httpx.Client() as client:
                        r = await getattr(client, method)(url, **kwargs)
                        status = r.status_code
                        try:
                            resp = r.json()
                        except Exception:
                            resp = r.text

                        if r.status_code == 429:
                            raise TooManyRequestsException(str(resp))
                        return resp, r.status_code
                except TooManyRequestsException:
                    tries += 1
                    w = random.uniform(0.8, 2)
                    await asyncio.sleep(w)
                except httpx.exceptions.ReadTimeout:
                    tries += 1
                    await asyncio.sleep(random.random())
                except Exception as e:
                    print(
                        f"[REQUEST_FAILED] something went wrong while calling {method} {url} with args: {kwargs} got error: {e} resp: {resp}, status: {status}!"
                    )
                    raise e
            # raise Exception()

    async def get(self, url, **kwargs):
        return await self._request("get", url, **kwargs)

    async def teardown(self):
        await self.close()
