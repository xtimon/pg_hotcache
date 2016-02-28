# pg_hotcache

Loading into cache from said PostgreSQL database the tables, which are most frequently scanned.

Limiter for loading into cache is the value of "effective_cache_size".

It makes sense to use after restarting the server!

Before using, you need to connect to the database as superuser and add the extension 'pg_prewarm' (added to PostgreSQL since version 9.4):

    create extension pg_prewarm;

Installation:

    pip install pg_hotcache
    
Alternative installation:

    git clone https://github.com/xtimon/pg_hotcache.git
    cd pg_hotcache
    python setup.py install
    
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
