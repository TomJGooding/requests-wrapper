from typing import Optional

import requests


class Session:
    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[dict] = None,
        auth_user: Optional[str] = None,
        auth_pass: Optional[str] = None,
        timeout: int = 10,
        raise_for_status: bool = True,
        max_retries: int = 0,
    ) -> None:
        self._url: Optional[str] = base_url
        self._headers: Optional[dict] = headers
        self._user: Optional[str] = auth_user
        self._pass: Optional[str] = auth_pass
        self._timeout: int = timeout
        self._raise_for_status: bool = raise_for_status
        self._max_retries: int = max_retries

    def _build_request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> requests.Request:
        url: str = self._url + path if self._url else path

        return requests.Request(method=method, url=url, **kwargs)
