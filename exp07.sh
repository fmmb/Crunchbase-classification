EXP=exp07.big-arffs
mkdir -p $EXP
cat exp01.42tags/most-relevant-words.txt| awk '{print $1}' > $EXP/most-relevant-words.txt

./bin/createarff.py $EXP/most-relevant-words.txt exp06.41tags/train.json.gz | gzip > $EXP/train.arff.gz
./bin/createarff.py -q $EXP/most-relevant-words.txt $EXP/train.arff.gz exp06.41tags/test.json.gz | gzip > $EXP/test.arff.gz
./bin/createarff.py -q $EXP/most-relevant-words.txt $EXP/train.arff.gz exp06.41tags/devel.json.gz | gzip > $EXP/devel.arff.gz

CLASSPATH=/Applications/Misc/weka-3-6-11
CLASSPATH=/afs/l2f/home/fmmb/usr/src/weka-3-6-9

CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomial)
CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomialUpdateable)
CLASSIFIER=(weka.classifiers.functions.SMO -C 1.0 -L 0.0010 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0")

java -Xmx6g -classpath $CLASSPATH/weka.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/devel.arff.gz > $EXP/devel.$(echo $CLASSIFIER[1] | sed -E 's/^[^ ]*\.//').txt

# For LibSVM use:
java -Xmx6g -cp $CLASSPATH/weka.jar:$CLASSPATH/libsvm.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/test.arff.gz
