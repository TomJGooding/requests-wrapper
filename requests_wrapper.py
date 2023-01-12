from typing import Optional

import requests


class Session:
    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[dict] = None,
        auth_user: Optional[str] = None,
        auth_pass: Optional[str] = None,
        timeout: float = 10,
        raise_for_status: bool = True,
        max_retries: int = 0,
    ) -> None:
        self._session: requests.Session = requests.Session()
        self._url: Optional[str] = base_url
        self._headers: Optional[dict] = headers
        self._user: Optional[str] = auth_user
        self._pass: Optional[str] = auth_pass
        self._timeout: float = timeout
        self._raise_for_status: bool = raise_for_status
        self._max_retries: int = max_retries

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        req: requests.Request = self._build_request(method, path, **kwargs)
        prepped: requests.PreparedRequest = req.prepare()
        try:
            resp: requests.Response = self._session.send(
                prepped,
                timeout=self._timeout,
            )
            if self._raise_for_status:
                resp.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise http_err
        except requests.exceptions.ConnectionError as cxn_err:
            raise cxn_err
        except requests.exceptions.Timeout as timeout_err:
            raise timeout_err
        except requests.exceptions.RequestException as req_err:
            raise req_err

        return resp

    def _build_request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> requests.Request:
        url: str = self._url + path if self._url else path

        return requests.Request(method=method, url=url, **kwargs)
