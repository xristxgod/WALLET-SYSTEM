import json
from typing import Dict, List
from datetime import datetime

import asyncio
import aiohttp
import aiofiles

from src.sender import Sender
from src.utils import Utils
from config import Config, ENDPOINTS_URL_PATH, logger

class Checker:

    @staticmethod
    async def request_status(**params):
        try:
            async with aiohttp.ClientSession(**params.get("session_params")) as session:
                async with session.__getattribute__(params.get("method"))(
                        params.get("_url"), **params.get("request_params")
                ) as response:
                    response: aiohttp.ClientResponse
                    if params.get("result_status") is not None:
                        if params.get("result_status") != response.status:
                            logger.error((
                                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ERROR: {params.get('title')}."
                                f" {params.get('_url')} | {await response.text()}"
                            ))
                            return False, lambda: Sender.send_news(
                                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                                message=(
                                    f"Invalid response status: {response.status}\n"
                                    f"Expected: {params.get('result_status')}"
                                )
                            )
                        if not response.ok:
                            logger.error((
                                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ERROR: {params.get('title')}."
                                f" {params.get('_url')} | {await response.text()}"
                            ))
                            return False, lambda: Sender.send_news(
                                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                                message=f'Request error: {response.status}\n'
                            )
                        else:
                            if params.get("json_query") is not None:
                                data: Dict = await response.json()
                                if isinstance(data, dict) and 'error' in data.keys():
                                    logger.error((
                                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ERROR: {params.get('title')}."
                                        f" {params.get('_url')} | {await response.text()}"
                                    ))
                                    return False, lambda: Sender.send_news(
                                        title=params.get("title"), url=params.get("_url"), tag=params.get("tag"),
                                        message=f"FALL. The response contains the 'error' field", is_error=True
                                    )
                                elif not await Utils.check_res(data, params.get("json_query")):
                                    logger.error((
                                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ERROR: {params.get('title')}."
                                        f" {params.get('_url')} | {await response.text()}"
                                    ))
                                    return False, lambda: Sender.send_news(
                                        title=params.get("title"), url=params.get("_url"), tag=params.get("tag"),
                                        message=f"FALL. Comparison with the sample", is_error=True
                                    )
                            return True, lambda: Sender.send_news(
                                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=False,
                                message=f"The problems have been fixed. Continuation of work in the previous mode"
                            )
        except Exception as error:
            logger.error(f'ERROR {params.get("title")}: {error}\n{params.get("_url")}')
            return False, lambda: Sender.send_news(
                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                message=f"Error on the bot's side"
            )

    @staticmethod
    async def check_endpoint(**params):
        session_params: Dict = Utils.get_headers(auth=params.get("auth"), headers=params.get("headers"))
        request_params = {"json": params.get("data_for_check")} if params.get("data_for_check") is not None else {}
        urls = Utils.get_url(params.get("url"), domains=Config.DOMAINS)
        is_work = True
        current_count_shutdowns = 0

        while True:
            result = [
                await Checker.request_status(
                    title=params.get("title"),
                    tag=params.get("tag"),
                    _url=_url,
                    session_params=session_params,
                    request_params=request_params,
                    json_query=params.get("json_query"),
                    method=params.get("method"),
                    result_status=params.get("result_status")
                )
                for _url in urls
            ]
            current_work = all(list(map(lambda x: x[0], result)))
            if params.get("count_checks") is not None:
                is_send = False
                if not current_work:
                    if not (current_count_shutdowns > params.get("count_checks")):
                        current_count_shutdowns += 1
                        is_send = current_count_shutdowns > params.get("count_checks")
                else:
                    is_send = current_count_shutdowns > params.get("count_checks")
                    current_count_shutdowns = 0
            else:
                is_send = True
            if is_work != current_work or params.get("count_checks") is not None:
                if is_send:
                    item = list(filter(lambda x: x[0] == current_work, result))[0]
                    await item[-1]()
                is_work = current_work
            await asyncio.sleep(params.get("delay_success") if is_work else params.get("delay_error"))

    @staticmethod
    async def check_all():
        async with aiofiles.open(ENDPOINTS_URL_PATH, 'r') as file:
            endpoints_url = json.loads(await file.read())
        await Sender.send_info(text='The bot for checking the system is running!')
        await asyncio.gather(*[Checker.check_endpoint(**url_params) for url_params in endpoints_url])