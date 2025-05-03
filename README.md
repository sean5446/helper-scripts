# Helper scripts

Helper scripts for Windows, Linux, Mac, raspberrypi, etc.

## One Liners

### HTTP Servers

`python3 -m http.server 8080`

`nohup php -S 0.0.0.0:8011 &`

### Remove Windows Characters
`perl -p -i -e 's/\r\n$/\n/g' file.sh`

### Postgres
`alias postgres_log="ls -l ../log/postgresql* | tail -n 1 | awk -F' ' '{print \$9}' | xargs tail -n 50 -f"`

`/opt/homebrew/opt/postgresql@13/bin/createuser -s postgres`

`/etc/init.d/postgresql status`

`sudo -u postgres psql`

`ALTER USER "postgres" WITH PASSWORD 'password';`

`\l` list database

`\c name` select database

`\dn` show schemas

`SET search_path TO schema_name;` set default schema

`\dt` list tables

`\df` show functions 

`\sf function_name` show function declaration

```
/opt/homebrew/var/postgresql@13/postgresql.conf
logging_collector = on
log_statement = 'mod'
```

### Apt
`dpkg -L` find location of installed package

`apt-cache search keyword`

`sudo dpkg -i package_file.deb` 

`sudo apt-get remove package_name`

### Zsh
`killport() { lsof -ti :$1 | xargs kill -9 }`

`jhome() { newhome=J_HOME$1; export JAVA_HOME=${(P)newhome}; file $JAVA_HOME }`

### Windows 
Remote Desktop Entries

`Computer\HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default`

Quick hard drive perf test

`winsat disk -drive g`

