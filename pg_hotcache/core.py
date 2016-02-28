import getpass
import psycopg2
import psycopg2.extras
import sys
from argparse import ArgumentParser
from re import compile


def load_cache(args):
    if not args.host:
        conn_string = "dbname='{}' user='{}' password='{}'".format(
            args.dbname, args.username, args.password
        )
    else:
        conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(
            args.host, args.port, args.dbname, args.username, args.password
        )
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.Error as e:
        if "password authentication failed" in str(e):
            password = getpass.getpass("Password for user {}: ".format(args.username))
            if not args.host:
                conn_string = "dbname='{}' user='{}' password='{}'".format(
                    args.dbname, args.username, password
                )
            else:
                conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(
                    args.host, args.port, args.dbname, args.username, password
                )
            try:
                conn = psycopg2.connect(conn_string)
            except psycopg2.Error as e:
                print(e)
                sys.exit(1)
        else:
            print(e)
            sys.exit(1)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("""SELECT version()""")
    except psycopg2.Error as e:
        print(e)
    rows = cur.fetchall()
    version = rows[0][0].split()[1].split('.')
    support_text = "Minimal supported PostgreSQL version is 9.4.\nYour PostgreSQL version is {}.{}.{}".format(*version)
    if version[0] == '9':
        if int(version[1]) < 4:
            print(support_text)
            sys.exit(1)
    if int(version[0]) < 9:
        print(support_text)
        sys.exit(1)
    B = {
        'kB': 1,
        'MB': 2,
        'GB': 3,
        'TB': 4
    }
    pg_units = compile(r'([\d])+({}|{}|{}|{})'.format(*B.keys()))
    try:
        cur.execute(
            """
            SELECT setting, unit
            FROM pg_settings
            WHERE name='effective_cache_size'
            """
        )
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)
    rows = cur.fetchall()
    eff_cache_size_setting = int(rows[0][0])
    eff_cache_size_unit = str(rows[0][1])
    unit_opts = pg_units.findall(eff_cache_size_unit)
    effective_cache_size = eff_cache_size_setting * int(unit_opts[0][0]) * 1024 ** B[unit_opts[0][1]]
    try:
        cur.execute(
            """
            SELECT relname, pg_relation_size(relid)
            FROM pg_stat_all_tables
            WHERE relname not like 'pg_%'
            ORDER BY COALESCE(seq_scan, 0)+COALESCE(idx_scan, 0) DESC;
            """
        )
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)
    rows = cur.fetchall()
    tables = list()
    i = 0
    summary_size = 0
    while summary_size < effective_cache_size:
        summary_size += rows[i][1]
        tables.append(rows[i][0])
        i += 1
    tables.pop()
    for table in tables:
        print("load table {} into cache".format(table))
        try:
            cur.execute(
                """
                select pg_prewarm('{}')
                """.format(table)
            )
        except psycopg2.Error as e:
            print(e)


def main():
    p = ArgumentParser(
        description='description',
        epilog='epilog',
        add_help=False,
    )
    p.add_argument('-?', '--help', action="help",
                   help="show this help message and exit")
    p.add_argument('-h', '--host', action='store',
                   help='database server host or socket directory (default: "local socket")')
    p.add_argument('-p', '--port', action='store', default=5432, type=int,
                   help='database server port (default: "5432")')
    p.add_argument('-U', '--username', action='store', default=getpass.getuser(),
                   help='database user name (default: "{}")'.format(getpass.getuser()))
    p.add_argument('-W', '--password', action='store',
                   help='force password prompt (should happen automatically)')
    p.add_argument('-d', '--dbname', action='store', default=getpass.getuser(),
                   help='database name to connect to (default: "{}")'.format(getpass.getuser()))
    args = p.parse_args()
    load_cache(args)

if __name__ == "__main__":
    main()
