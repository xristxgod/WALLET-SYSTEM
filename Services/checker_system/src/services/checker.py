import asyncio
from typing import Dict

import aiohttp

from src.services.sender import Bot
from src.services.__init__ import Endpoint
from src.utils import CheckerUtils, Errors
from config import Config, logger

class Checker:

    @staticmethod
    async def __check_result(data, query_list):
        try:
            q_len = len(query_list)
            if q_len == 0:
                return True
            else:
                if q_len == 1:
                    query, result = query_list[0].split('=')
                    result = await CheckerUtils.str_to_coded_type(result)
                    return data[query] == result
                else:
                    field: str = query_list[0]
                    if field.isdigit():
                        return await Checker.__check_result(data[int(field)], query_list[1:])
                    else:
                        return await Checker.__check_result(data[field], query_list[1:])
        except Exception as error:
            logger.error(f'ERROR: {error}. DATA: {data}. QUERY: {query_list}')
            await Errors.write_to_error(error=error, msg="ERROR CHECKER STEP 16")
            return False

    @staticmethod
    async def check_result(data, queries):
        if len(queries) == 0 or queries is None:
            return True
        result = all([await Checker.__check_result(data, q.split('.')) for q in queries])
        if not result:
            logger.error(f'NEW: {data}. QUERY: {queries}')
        return result

    @staticmethod
    async def request_status(is_send: bool = True, **params):
        try:
            async with aiohttp.ClientSession(**params.get("session_params")) as session:
                async with session.__getattribute__(params.get("method"))(params.get("_url"), **params.get("request_params")) as response:
                    response: aiohttp.ClientResponse
                    if params.get("result_status") is not None:
                        if params.get("result_status") != response.status:
                            logger.error(
                                f"Invalid response status: {response.status} | Expected: {params.get('result_status')}"
                            )
                            if is_send:
                                return False, lambda: Bot.send_report(
                                    title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                                    message=f'Invalid response status: {response.status}\n'
                                            f'Expected: {params.get("result_status")}'
                                )
                    if not response.ok:
                        logger.error(f'Request error: {response.status}')
                        if is_send:
                            return False, lambda: Bot.send_report(
                                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                                message=f'Request error: {response.status}\n'
                            )
                    else:
                        if params.get("json_query") is not None:
                            data: dict = await response.json()
                            if isinstance(data, dict) and 'error' in data.keys():
                                logger.error("Fall. The response contains the 'error' field")
                                if is_send:
                                    return False, lambda: Bot.send_report(
                                        title=params.get("title"), url=params.get("_url"), tag=params.get("tag"),
                                        message=f'Fall. The response contains the "error" field', is_error=True
                                    )
                            elif not await Checker.check_result(data, params.get("json_query")):
                                logger.error("Fall. Comparison with the sample")
                                if is_send:
                                    return False, lambda: Bot.send_report(
                                        title=params.get("title"), url=params.get("_url"), tag=params.get("tag"),
                                        message=f'Fall. Comparison with the sample', is_error=True
                                    )
                        logger.error('The problems have been fixed. Continuation of work in the previous mode')
                        if is_send:
                            return True, lambda: Bot.send_report(
                                title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=False,
                                message=f'The problems have been fixed. Continuation of work in the previous mode'
                            )
        except Exception as error:
            logger.error(f'ERROR {params.get("title")}: {error}\n{params.get("_url")}')
            await Errors.write_to_error(error=error, msg="ERROR CHECKER STEP 48")
            if is_send:
                return False, lambda: Bot.send_report(
                    title=params.get("title"), url=params.get("_url"), tag=params.get("tag"), is_error=True,
                    message="'Error on the bot side'"
                )

    @staticmethod
    async def url_param_to_list(param: str):
        start = param.find('{{')
        end = param.find('}}')
        if start != -1 and end != -1:
            params = param[start + 2: end].split('||')
            urls = [
                f'{param[:start]}{_param}{param[end + 2:]}'
                for _param in params
            ]
        else:
            urls = [param]
        return [u.format(**Config.DOMAINS) for u in urls]

    @staticmethod
    async def check_endpoint(is_send: bool = True, **params):
        session_params = CheckerUtils.get_headers(params.get("auth"), headers=params.get("headers"))
        request_params = CheckerUtils.get_request_params(params.get("data_for_check"))
        urls = await Checker.url_param_to_list(params.get("url"))
        is_work = True
        while True:
            result = [
                await Checker.request_status(
                    is_send=is_send,
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
            if is_work != current_work:
                item = list(filter(lambda x: x[0] == current_work, result))[0]
                await item[-1]()
                is_work = current_work
            await asyncio.sleep(params.get("delay_success") if is_work else params.get("delay_error"))

async def check_all(is_all: bool = True, is_send: bool = True, sub: str = None, mod: str = None,):
    if is_all:
        endpoints = await Endpoint.get_all_endpoints()
    else:
        endpoints = await Endpoint.get_endpoints(sub_name=sub, mod_name=mod)

    logger.error("::::CHECKER BOT HAS STARTED WORKING::::")
    if is_send:
        await Bot.send_to_bot(CheckerUtils.get_hello_text())
    await asyncio.gather(*[
        Checker.check_endpoint(is_send=is_send, **endpoint_params)
        for endpoint_params in endpoints
    ])

async def run():
    await check_all()

if __name__ == '__main__':
    asyncio.run(run())