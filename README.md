# pg_hotcache
## Loading into cache from said PostgreSQL database the tables, which are most frequently scanned.
## Limiter for loading into cache is the value of "effective_cache_size".

Installation:

    pip install pg_hotcache
    
usage:

    pg_hotcache [-?] [-h HOST] [-p PORT] [-U USERNAME] [-W PASSWORD] -d DBNAME

optional arguments:

    -?, --help            show this help message and exit
    -h HOST, --host HOST  database server host or socket directory (default:
                          "local socket")
    -p PORT, --port PORT  database server port (default: "5432")
    -U USERNAME, --username USERNAME
                          database user name (default: "bars")
    -W PASSWORD, --password PASSWORD
                          force password prompt (should happen automatically)
    -d DBNAME, --dbname DBNAME
                          database name for caching

examples:

    sudo -u postgres pg_hotcache -d dbname
    pg_hotcache -h 127.0.0.1 -p 5432 -U username -d dbname
