from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import app.config as config
from app.status import status_store


class ApiHandler(BaseHTTPRequestHandler):
    """HTTP API for the Internet Monitor."""

    server_version = (
        f"{config.APP_NAME}/{config.APP_VERSION}"
    )

    # -------------------------------------------------------------------------

    def do_GET(self) -> None:

        if self.path == "/status":

            self._send_status()

            return

        self.send_error(404, "Not Found")

    # -------------------------------------------------------------------------

    def _send_status(self) -> None:

        body = json.dumps(
            status_store.get(),
            indent=4,
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json",
        )

        self.send_header(
            "Content-Length",
            str(len(body)),
        )

        self.end_headers()

        self.wfile.write(body)

    # -------------------------------------------------------------------------

    def log_message(
        self,
        format: str,
        *args,
    ) -> None:
        """
        Disable default HTTP logging.

        All logging is handled by the application logger.
        """
        return


# =============================================================================
# Public API
# =============================================================================


def start_api() -> None:
    """Start the REST API."""

    server = ThreadingHTTPServer(
        (
            config.API_HOST,
            config.API_PORT,
        ),
        ApiHandler,
    )

    server.serve_forever()