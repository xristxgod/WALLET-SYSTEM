from typing import Dict

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