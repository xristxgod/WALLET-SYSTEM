from typing import Dict

from config import logger

class Utils:
    @staticmethod
    def get_headers(headers: Dict = None, auth: str = None) -> Dict:
        if auth is None:
            session_params = {"headers": {"Authorization": auth}}
        else:
            session_params = {}
        if headers is not None:
            if "headers" in session_params:
                session_params["headers"].update(headers)
            else:
                session_params = {"headers": headers}
        return session_params

    @staticmethod
    def get_url(urls: str, domains: Dict):
        return [url.format(**domains) for url in [urls]]

    @staticmethod
    def str_to_coded_type(s: str):
        t, value = s.split('_')
        if t == 'str':
            return value
        elif t == 'int':
            return int(value)
        elif t == 'bool':
            return value.lower() == 'true'
        return value

    @staticmethod
    def check_result(data, query_list):
        try:
            q_len = len(query_list)
            if q_len == 0:
                return True
            else:
                if q_len == 1:
                    query, result = query_list[0].split('=')
                    result = Utils.str_to_coded_type(result)
                    return data[query] == result
                else:
                    field: str = query_list[0]
                    if field.isdigit():
                        return await Utils.check_result(data[int(field)], query_list[1:])
                    else:
                        return await Utils.check_result(data[field], query_list[1:])
        except Exception as e:
            logger.error(f'ERROR: {e}. DATA: {data}. QUERY: {query_list}')
            return False

    @staticmethod
    def check_res(data, queries):
        if len(queries) == 0 or queries is None:
            return True
        result = all([Utils.check_result(data, q.split('.')) for q in queries])
        if not result:
            logger.error(f'NEW: {data}. QUERY: {queries}')
        return result