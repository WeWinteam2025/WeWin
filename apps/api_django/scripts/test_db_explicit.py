import os
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    user = os.getenv("user") or os.getenv("PGUSER")
    password = os.getenv("password") or os.getenv("PGPASSWORD")
    host = os.getenv("host") or os.getenv("PGHOST")
    port = int(os.getenv("port") or os.getenv("PGPORT") or 5432)
    dbname = os.getenv("dbname") or os.getenv("PGDATABASE") or "postgres"
    print("Params:", {"user": user, "host": host, "port": port, "dbname": dbname})

    try:
        import psycopg

        conn = psycopg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=dbname,
            connect_timeout=5,
            sslmode="require",
        )
        with conn.cursor() as cur:
            cur.execute("select 1")
            print("CONNECTION_OK", cur.fetchone())
        conn.close()
    except Exception as e:  # noqa: BLE001
        print("CONNECTION_ERR", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()





