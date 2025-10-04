import os
import socket
from urllib.parse import urlparse

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("DATABASE_URL not set")
        raise SystemExit(2)

    parsed = urlparse(dsn)
    host = parsed.hostname or ""
    port = parsed.port or 5432
    print(f"Host: {host}")
    print(f"Port: {port}")

    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
        fams = sorted({info[0] for info in infos})
        print("getaddrinfo families:", [
            "IPv4" if f == socket.AF_INET else "IPv6" if f == socket.AF_INET6 else str(f)
            for f in fams
        ])
        addrs = sorted({info[4][0] for info in infos})
        print("Resolved addresses:", addrs)
    except Exception as e:
        print("DNS/Resolution error:", e)

    try:
        import psycopg

        print("Connecting with psycopg ...")
        conn = psycopg.connect(dsn, connect_timeout=5, sslmode="require")
        with conn.cursor() as cur:
            cur.execute("select 1")
            row = cur.fetchone()
        conn.close()
        print("CONNECTION_OK", row)
    except Exception as e:  # noqa: BLE001
        print("CONNECTION_ERR", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()




