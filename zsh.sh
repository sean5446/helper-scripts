
# funcs
killport() { lsof -ti :$1 | xargs kill -9 }
jhome() { newhome=J_HOME$1; export JAVA_HOME=${(P)newhome}; echo $JAVA_HOME }
hunt()  { grep -rn  --include='*.sql' --include='*.java' "$1" | grep -v serialVersionUID | grep "$1" }
ihunt() { grep -rni --include='*.sql' --include='*.java' "$1" | grep -v serialVersionUID | grep -i "$1" }

# general - don't overwrite stuff without asking
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'


# tomcat mgmt
alias tomcat_status='ps aux | grep "[t]omcat" | grep -v embed | awk -F'\'' '\'' '\''{print $2}'\'' | grep . '
alias tomcat_down='tomcat_status | xargs kill -9'
alias tomcat_up="$CATALINA_HOME/bin/startup.sh"
alias tomcat_restart='tomcat_down && tomcat_up'
alias tomcat_log="tail -n 300 -f $CATALINA_HOME/logs/catalina.out"
alias tomcat_config="code $CATALINA_HOME/conf/Catalina/localhost/"
alias tomcat_env="code $CATALINA_HOME/bin/setenv.sh"

# plm
alias plm_restart="touch $CATALINA_HOME/webapps/predev-tools-2022r1/WEB-INF/web.xml && echo RESTART > $CATALINA_HOME/logs/catalina.out"
alias plm_nuke="tomcat_down && rm -rf $CATALINA_HOME/{predev-tools-2022r1,webapps/predev-tools-2022r1,tradeengines-logfile.log,logs/*}"

# postgres
alias postgres_log="ls -l /opt/homebrew/var/postgresql@13/log/postgresql* | tail -n 1 | awk -F' ' '{print \$9}' | xargs tail -n 50 -f"
alias postgres_config="code /opt/homebrew/var/postgresql@13/postgresql.conf"
