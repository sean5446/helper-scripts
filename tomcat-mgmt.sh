#!/bin/bash

# tomcat mgmt
alias tomcat_status='ps aux | grep "[t]omcat" | awk -F '\'' '\'' '\''{print $2}'\'' | grep . '
alias tomcat_down='tomcat_status | xargs kill -9'
alias tomcat_up="$CATALINA_HOME/bin/startup.sh"
alias tomcat_log="tail -n 300 -f $CATALINA_HOME/logs/catalina.out"
