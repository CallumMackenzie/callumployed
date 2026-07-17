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
from callumployed.data.repositories import get_tracking_stats, list_role_items

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
        self.server_name = str(self.server_address[0])
        self.server_port = int(self.server_address[1])


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

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_json(self, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

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
    return "application/octet-stream"
