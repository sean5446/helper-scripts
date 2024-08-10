# Helper scripts

Helper scripts for Windows, Linux, Mac, raspberrypi, etc.

## One Liners

### Python HTTP Server

`python3 -m http.server 8080`

### PHP HTTP Server

`nohup php -S 0.0.0.0:8011 &`

### Postgres
`alias postgres_log="ls -l ../log/postgresql* | tail -n 1 | awk -F' ' '{print \$9}' | xargs tail -n 50 -f"`

`/opt/homebrew/opt/postgresql@13/bin/createuser -s postgres`

`/etc/init.d/postgresql status`

`sudo -u postgres psql`

`ALTER USER "postgres" WITH PASSWORD 'password';`

`\l` list database

`\c name` select database

`\dt` list tables

```
/opt/homebrew/var/postgresql@13/postgresql.conf
logging_collector = on
log_statement = 'mod'
```

### Packages
`dpkg -L` find location of installed package

`apt-cache search keyword`

`sudo dpkg -i package_file.deb` 

`sudo apt-get remove package_name`

### Zsh
`killport() { lsof -ti :$1 | xargs kill -9 }`

`jhome() { newhome=J_HOME$1; export JAVA_HOME=${(P)newhome}; file $JAVA_HOME }`

