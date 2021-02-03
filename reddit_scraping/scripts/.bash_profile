#!bash
#prints out wisdom saying
CN=$(wc -l ~/.data/quotes.csv | awk '{print $1}')
LINE=$((RANDOM % $CN +2))
QUOTE=$(sed -n "${LINE}p" ~/.data/quotes.csv | grep -o '".*."' | sed 's/".*","/"/g')
AUTH=$(sed -n "${LINE}p" ~/.data/quotes.csv | grep -o '".*",' | sed 's/"//g' | sed 's/,//g')
echo $QUOTE
echo '~ '$AUTH
