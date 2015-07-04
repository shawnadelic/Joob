for i in {1..299}
do
    b=$(printf %03d ${i})
    grep -v '^$' $b > $b.txt
done
