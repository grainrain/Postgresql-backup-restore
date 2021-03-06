import json
import os
import sys

if len(sys.argv) < 2:
    print('Usage:\n', sys.argv[0],
          '\ndev_all\n'
          + 'dev_keycloak\n'
          + 'dev_masterdata\n'
          )
    exit()
dbparam = sys.argv[1]

print('------------>' + dbparam)

with open(os.getcwd() + os.sep + 'restore.json') as conf_file:
    # with open(os.path.dirname(__file__) + os.sep + 'env-conf.json') as conf_file:
    backup_conf = json.load(conf_file)


def set_env_param(dbparam):
    host = backup_conf[dbparam]['host']
    port = backup_conf[dbparam]['port']
    db_name = backup_conf[dbparam]['database']
    username = backup_conf[dbparam]['username']
    password = backup_conf[dbparam]['password']
    return GenBat(host, port, db_name, username, password)


def GenBat(host, port, db_name, username, password):
    strbuf = ('@echo off' + '\n'
              + '' + '\n'
              + 'echo ">>>>>>host[' + host + '],port[' + port + '],dbname[' + db_name + ']begin to restore' + '<<<<<<"' + '\n'
              + '' + '\n'
              + 'for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if \'.%%i.\'==\'.LocalDateTime.\' set ldt=%%j' + '\n'
              + '' + '\n'
              + 'set curdate=%ldt:~0,4%%ldt:~4,2%%ldt:~6,2%' + '\n'
              + 'SET PGPASSWORD=' + password + '\n'
              + 'SET db_name=' + db_name + '\n'
              + 'SET encoding=UTF-8' + '\n'
              + 'SET host=' + host + '\n'
              + 'SET port=' + port + '\n'
              + 'SET username=' + username + '\n'
              + 'SET rolename=' + username + '\n'
              + 'SET pg_restore_path="C:\\local\\pgsql7\\bin\\pg_restore.exe"' + '\n'
              + 'SET backup_path=\\\\devhost\\DB_Backup\\%curdate%\\' + '\n'
              + 'SET other_flags=--verbose  ' + '\n'
              + 'SET backup_file=%backup_path%%db_name%_%curdate%.backup' + '\n'
              + '%pg_restore_path%  --format=c  -n "public" -h %host%   -p %port% --role=%rolename%  -U %username%  -d %db_name% -n public  %other_flags% %backup_file% ' + '\n'
              # + 'timeout /T 10 /NOBREAK' + '\n'
              + '' + '\n'
              )
    return strbuf


if dbparam == 'dev_all':
    dbparamall = ['dev_keycloak',
                  'dev_masterdata',
                 ]
    for db_param_single in dbparamall:
        badkup_bat_path = db_param_single + '.bat'
        with open(badkup_bat_path, 'w') as f:
            content = set_env_param(db_param_single)
            f.write(content)
    with open('dev_all_restore.bat', 'w') as f:
        content = ('@echo off' + '\n'
                   + 'for /f "tokens=* delims=" %%a in (\' dir /b /s %~dp0\\dev_*.bat^| find /v "dev_all"\') do ( call %%a)' + '\n')
        f.write(content)
else:
    badkup_bat_path = dbparam + '.bat'
    with open(badkup_bat_path, 'w') as f:
        content = set_env_param(dbparam)
        f.write(content)
