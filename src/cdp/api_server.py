import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "cdp.db"


class CustomerAPIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")

        if len(parts) != 3 or parts[0] != "customers" or parts[2] != "summary":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        customer_id = parts[1]

        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row

        try:
            customer = connection.execute(
                """
                SELECT
                    customer_id,
                    customer_name,
                    account_count,
                    transaction_count,
                    total_transaction_amount,
                    last_transaction_date
                FROM customer_360
                WHERE customer_id = ?
                """,
                (customer_id,)
            ).fetchone()

            if customer is None:
                self.send_json(404, {"error": "Customer not found"})
                return

            self.send_json(200, dict(customer))

        finally:
            connection.close()

    def send_json(self, status_code, data):
        response = json.dumps(data, indent=4).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def start_server():
    server = HTTPServer(
        ("127.0.0.1", 8000),
        CustomerAPIHandler
    )

    print("Customer 360 API is running!")
    print("Address: http://127.0.0.1:8000")
    print("Press CTRL+C to stop the server.")

    server.serve_forever()


if __name__ == "__main__":
    start_server()