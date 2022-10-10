# 2015-03
#    Trying to see if the two different fingerprints give different results for different text lenghts
#
EXP=exp08.ffp_description_size
mkdir -p $EXP

# filters by selected tags (Skips "other")
./bin/group_tags.py ./exp01.42tags/train_dev_test.json.gz | gzip > $EXP/train_dev_test.json.gz
./bin/group_tags.py ./exp01.42tags/train_devel.json.gz | gzip > $EXP/train_devel.json.gz
./bin/group_tags.py ./exp01.42tags/train.json.gz | gzip > $EXP/train.json.gz
./bin/group_tags.py ./exp01.42tags/devel.json.gz | gzip > $EXP/devel.json.gz
./bin/group_tags.py ./exp01.42tags/test.json.gz | gzip > $EXP/test.json.gz

# Extracting the reference
./bin/extract_info.py -q $EXP/devel.json.gz -tag > $EXP/devel.ref
./bin/extract_info.py -q $EXP/test.json.gz -tag > $EXP/test.ref

# train and evaluate
# ---------------------------------------------------------------------------------------------------
./bin/topic_fingerpr.py -k=4000 $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref


# Results by number of words for FINGERPRINTS and FINGERPRINTS2
# ----------------
./bin/extract_info.py $EXP/devel.json.gz -desclen  > 0.txt
for k in 100 500 4000; do
  time ./bin/topic_fingerpr.py -k=$k $EXP/train.json.gz $EXP/devel.json.gz > $k
done
paste 0.txt 100 | awk '{if($1==$3){print $2,"c"}else{print $2,"i"}}' |  sort -g | uniq -c | awk '{if($2!=p){print p, c, i;i=0;c=0;p=$2}; if($3=="i"){i=$1}else{c=$1} }END{print p, c, i}'

# Multinomial Naive Bayes
# ------------------------
# Used freqmin=3
./bin/extract_info.py -q exp01.42tags/train_devel.json.gz  -tfidf | awk '{print $1}' > $EXP/most-relevant-words.txt

./bin/createarff.py $EXP/most-relevant-words.txt $EXP/train.json.gz | gzip > $EXP/train.arff.gz
./bin/createarff.py -q $EXP/most-relevant-words.txt $EXP/train.arff.gz $EXP/test.json.gz | gzip > $EXP/test.arff.gz
./bin/createarff.py -q $EXP/most-relevant-words.txt $EXP/train.arff.gz $EXP/devel.json.gz | gzip > $EXP/devel.arff.gz

CLASSPATH=/Applications/Misc/weka-3-6-11
CLASSPATH=/afs/l2f/home/fmmb/usr/src/weka-3-6-9

CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomial)
CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomialUpdateable)
CLASSIFIER=(weka.classifiers.functions.SMO -C 1.0 -L 0.0010 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0")

java -Xmx6g -classpath $CLASSPATH/weka.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/devel.arff.gz > $EXP/devel.$(echo $CLASSIFIER[1] | sed -E 's/^[^ ]*\.//').txt

# For LibSVM use:
java -Xmx6g -cp $CLASSPATH/weka.jar:$CLASSPATH/libsvm.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/test.arff.gz

# Measuring the performance by number of words:
./bin/extract_info.py $EXP/devel.json.gz -desclen | awk '{print $2}' > 0.txt
java -Xmx6g -classpath $CLASSPATH/weka.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/devel.arff.gz -p last > 1.txt
cat 1.txt | awk '/^ *[0-9]/{if($2==$3){print "c"}else{print "i"}}' | paste 0.txt - | sort -g | uniq -c | awk '{if($2!=p){print p, c, i;i=0;c=0;p=$2}; if($3=="i"){i=$1}else{c=$1} }END{print p, c, i}' | less



