from __future__ import absolute_import, print_function

import asyncio


from typing import Any, Dict, Tuple

import httpx


from pydantic import BaseModel

# import aiohttp


class Session(BaseModel):
    sem: Any = None
    semaphore: int = None
    max_tries: int = 5

    async def setup(self):
        if self.semaphore:
            self.sem = asyncio.Semaphore(self.semaphore)
        else:
            self.sem = asyncio.Semaphore(250)

    async def teardown(self):
        pass

    async def _request(self, method, url, receive_cookies=False, receive_headers=False, **kwargs):
        method = method.lower()
        tries = 0
        while tries < self.max_tries:
            try:
                async with self.sem:
                    async with httpx.Client() as session:
                        async with getattr(session, method)(url, **kwargs) as resp:
                            status = resp.status
                            respcookies = resp.cookies
                            respheaders = resp.headers
                            response = await resp.json()
                        if receive_cookies:
                            return response, status, respcookies
                        if receive_headers:
                            return response, status, respheaders
                        if receive_headers and receive_cookies:
                            return response, status, respheaders, respcookies
                        return response, status
            # except aiohttp.client_exceptions.ClientOSError as e:
            #     print(f"[SESSION_CLIENT_OS_ERROR] error: {e} retrying requests: {method} {url}, {kwargs}")
            #     tries += 1
            #     await asyncio.sleep(random.random())
            except Exception as e:
                print("==========================")
                print(f"[REQUEST_FAILED] {method} {url} {kwargs}")
                print("==========================")
                print(e)
                print(e)
                print(e)
                print(e)
                print("==========================")
                raise e from e

    async def get(self, url, **kwargs):
        return await self._request("get", url, **kwargs)

    async def post(self, url, **kwargs):
        return await self._request("post", url, **kwargs)

    async def put(self, url, **kwargs):
        return await self._request("put", url, **kwargs)

    async def patch(self, url, **kwargs):
        return await self._request("patch", url, **kwargs)


class SessionWrapper(BaseModel):
    s: Session = None


class ApiAuzWrapper(BaseModel):
    host: str
    session: SessionWrapper

    async def check_if_allowed(self, body: Dict[Any, Any], headers: Dict[Any, Any]) -> Tuple[Dict[str, bool], int]:
        """
        return a dict {"allowed": <bool>, "auz_token": <str>} with status 200 | 400
        """
        resp, status = await self.session.s.post(self.host + "/v1/api/allowed", json=body, headers=headers)
        return resp, status
