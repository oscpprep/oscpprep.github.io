!/bin/bash

echo "usage : ./finger_enum.sh <ip> <user_list.txt>"

user=$2
ping -c 3 $1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
        echo "-- target reachable";
else
        echo "-- target not reachable -end of execution";
        kill -9 $$
fi

for line in $(cat $user); do

        finger $line@$1 | grep "Login" > /dev/null 2>&1;
        if [ $? -eq 0 ];then
                echo " $line on $1 is valid user";
        fi
done



