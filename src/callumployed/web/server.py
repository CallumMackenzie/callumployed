from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import PurePosixPath
from socketserver import BaseServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from callumployed.data import db
from callumployed.data.models import RoleStatus
from callumployed.data.repositories import (
    get_tracking_stats,
    list_role_items,
    record_role_review_later,
    set_role_status,
)

STATIC_PACKAGE = "callumployed.web.static"
STATUS_LABELS: dict[str, str] = {
    RoleStatus.DISCOVERED.value: "Discovered",
    RoleStatus.INTERESTED.value: "Interested",
    RoleStatus.DISINTERESTED.value: "Disinterested",
    RoleStatus.PREPARED.value: "Prepared",
    RoleStatus.APPLIED.value: "Applied",
    RoleStatus.OA.value: "OA",
    RoleStatus.INTERVIEW.value: "Interview",
    RoleStatus.REJECTED.value: "Rejected",
    RoleStatus.OFFER.value: "Offer",
    RoleStatus.CLOSED.value: "Closed",
    RoleStatus.ARCHIVED.value: "Archived",
}


class LocalThreadingHTTPServer(ThreadingHTTPServer):
    def server_bind(self) -> None:
        self.socket.bind(self.server_address)
        host, port = self.socket.getsockname()[:2]
        self.server_address = (host, port)
        self.server_name = str(host)
        self.server_port = int(port)


def build_tracker_payload(query: str | None = None) -> dict[str, Any]:
    with db.connect() as connection:
        stats = get_tracking_stats(connection)
        roles = list_role_items(connection, query=query)

    grouped_roles: dict[str, list[dict[str, Any]]] = {status.value: [] for status in RoleStatus}
    for role in roles:
        grouped_roles[role.role_status.value].append(role.model_dump(mode="json"))

    statuses = [
        {
            "key": status.value,
            "label": STATUS_LABELS[status.value],
            "count": len(grouped_roles[status.value]),
            "jobs": grouped_roles[status.value],
        }
        for status in RoleStatus
    ]

    return {
        "stats": stats,
        "statuses": statuses,
        "query": query or "",
    }


def create_handler() -> type[BaseHTTPRequestHandler]:
    class CallumployedHandler(BaseHTTPRequestHandler):
        server_version = "callumployed"

        def do_GET(self) -> None:
            parsed_url = urlparse(self.path)
            if parsed_url.path in {"/", "/index.html"}:
                self._send_static_file("index.html", "text/html; charset=utf-8")
                return
            if parsed_url.path == "/api/tracker":
                query_values = parse_qs(parsed_url.query).get("q", [""])
                query = query_values[0].strip() or None
                self._send_json(build_tracker_payload(query=query))
                return
            if parsed_url.path.startswith("/assets/"):
                filename = PurePosixPath(parsed_url.path).name
                content_type = _content_type_for(filename)
                self._send_static_file(filename, content_type)
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            parsed_url = urlparse(self.path)
            path_parts = [part for part in PurePosixPath(parsed_url.path).parts if part != "/"]
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "status"
            ):
                self._update_role_status(path_parts[2])
                return
            if (
                len(path_parts) == 4
                and path_parts[0] == "api"
                and path_parts[1] == "roles"
                and path_parts[3] == "review-later"
            ):
                self._record_review_later(path_parts[2])
                return
            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_json(self, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json_body(self) -> dict[str, Any] | None:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return {}
            try:
                payload = json.loads(self.rfile.read(length).decode())
            except json.JSONDecodeError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON body")
                return None
            if not isinstance(payload, dict):
                self.send_error(HTTPStatus.BAD_REQUEST, "JSON body must be an object")
                return None
            return payload

        def _update_role_status(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            payload = self._read_json_body()
            if payload is None:
                return
            status_value = payload.get("status")
            try:
                status = RoleStatus(status_value)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role status")
                return

            if status not in {
                RoleStatus.APPLIED,
                RoleStatus.CLOSED,
                RoleStatus.DISINTERESTED,
                RoleStatus.INTERESTED,
                RoleStatus.INTERVIEW,
                RoleStatus.OA,
                RoleStatus.OFFER,
                RoleStatus.REJECTED,
            }:
                self.send_error(HTTPStatus.BAD_REQUEST, "Unsupported role status")
                return

            try:
                with db.connect() as connection:
                    role = set_role_status(
                        connection,
                        role_id,
                        status,
                        summary="Status updated from tracker.",
                    )
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            self._send_json({"role": role.model_dump(mode="json")})

        def _record_review_later(self, role_id_text: str) -> None:
            try:
                role_id = int(role_id_text)
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Invalid role ID")
                return

            try:
                with db.connect() as connection:
                    role = record_role_review_later(connection, role_id)
            except LookupError:
                self.send_error(HTTPStatus.NOT_FOUND, "Role not found")
                return

            self._send_json({"role": role.model_dump(mode="json")})

        def _send_static_file(self, filename: str, content_type: str) -> None:
            try:
                body = resources.files(STATIC_PACKAGE).joinpath(filename).read_bytes()
            except FileNotFoundError:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return CallumployedHandler


def run_server(host: str, port: int) -> None:
    db.ensure_initialized()
    handler = create_handler()
    server = LocalThreadingHTTPServer((host, port), handler)
    try:
        server.serve_forever()
    finally:
        _close_server(server)


def _close_server(server: BaseServer) -> None:
    server.server_close()


def _content_type_for(filename: str) -> str:
    if filename.endswith(".css"):
        return "text/css; charset=utf-8"
    if filename.endswith(".js"):
        return "text/javascript; charset=utf-8"
    if filename.endswith(".svg"):
        return "image/svg+xml; charset=utf-8"
    return "application/octet-stream"
