from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import app.config as config
from app.status import status_as_dict


class ApiHandler(BaseHTTPRequestHandler):

    server_version = (
        f"{config.APP_NAME}/{config.APP_VERSION}"
    )

    def do_GET(self) -> None:

        if self.path != "/status":

            self.send_error(404)

            return

        body = json.dumps(
            status_as_dict(),
            indent=4,
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(body)),
        )

        self.end_headers()

        self.wfile.write(body)

    def log_message(
        self,
        *_,
    ) -> None:
        return


def start_api() -> None:

    server = ThreadingHTTPServer(
        (
            config.API_HOST,
            config.API_PORT,
        ),
        ApiHandler,
    )

    server.serve_forever()