# regression tests
while read CORE START
do
    XCORE=`python cores.py --cores $START`
    if [ $XCORE -ne $CORE ]
    then
        echo "$START: $XCORE ≠ $CORE" >&2
    fi
done <<EOF
18 86455
14 3614
53 M CC XI II
3 MCCXIII
7 54321
11 654321
23 7654321
7 9876543212345
EOF
