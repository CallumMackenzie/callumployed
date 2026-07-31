from collections.abc import Sequence

import httpx

from callumployed.central.models import (
    BulkUpsertRole,
    BulkUpsertRolesRequest,
    BulkUpsertRolesResponse,
    CentralRolesResponse,
    ResolveCompanyRequest,
    ResolveCompanyResponse,
)


class CentralStoreError(RuntimeError):
    """Raised when the central store cannot complete a request."""


class CentralStoreClient:
    def __init__(
        self,
        *,
        api_url: str,
        passkey: str | None = None,
        timeout: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:
        self._api_url = api_url.rstrip("/")
        self._passkey = passkey
        self._timeout = timeout
        self._client = client

    def resolve_company(self, request: ResolveCompanyRequest) -> ResolveCompanyResponse:
        return ResolveCompanyResponse.model_validate(
            self._request("POST", "/v1/companies/resolve", json=request.model_dump())
        )

    def list_roles(self) -> CentralRolesResponse:
        return CentralRolesResponse.model_validate(self._request("GET", "/v1/roles"))

    def bulk_upsert_roles(
        self,
        roles: Sequence[BulkUpsertRole],
    ) -> BulkUpsertRolesResponse:
        request = BulkUpsertRolesRequest(roles=list(roles))
        return BulkUpsertRolesResponse.model_validate(
            self._request("POST", "/v1/roles/bulk-upsert", json=request.model_dump())
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: object | None = None,
    ) -> dict[str, object]:
        try:
            if self._client is None:
                with httpx.Client(timeout=self._timeout) as client:
                    response = client.request(
                        method,
                        f"{self._api_url}{path}",
                        headers=self._headers(),
                        json=json,
                    )
            else:
                response = self._client.request(
                    method,
                    f"{self._api_url}{path}",
                    headers=self._headers(),
                    json=json,
                )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise CentralStoreError(
                f"central store returned {error.response.status_code}: {error.response.text}"
            ) from error
        except httpx.HTTPError as error:
            raise CentralStoreError(f"central store request failed: {error}") from error

        data = response.json()
        if not isinstance(data, dict):
            raise CentralStoreError("central store returned a non-object JSON response")
        return data

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self._passkey is not None:
            headers["X-Callumployed-Passkey"] = self._passkey
        return headers
