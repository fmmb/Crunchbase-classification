# Initial experiment using all tags

EXP=exp01.42tags
mkdir -p $EXP

# filters by selected tags and randomizes data
./bin/select_and_rand.py data/companies-info.json.gz | gzip > $EXP/train_dev_test.json.gz

# Manually split the data (please check if test starts with the token "COMPANY")
tot=$(zcat $EXP/train_dev_test.json.gz | wc -l)
trn=$(echo "($tot * 0.70)/1" | bc)
tst=$(echo "($tot * 0.15)/1" | bc)
zcat $EXP/train_dev_test.json.gz | head -$(($tot-$tst)) | gzip > $EXP/train_devel.json.gz
zcat $EXP/train_devel.json.gz | head -$trn | gzip > $EXP/train.json.gz
zcat $EXP/train_devel.json.gz | tail +$(($trn+1)) | gzip > $EXP/devel.json.gz
zcat $EXP/train_dev_test.json.gz | tail -$tst | gzip > $EXP/test.json.gz

# Statistics about the TAGS
./bin/extract_info.py -tag $EXP/train_dev_test.json.gz | sort | uniq -c
# extracts the text
./bin/extract_info.py -description $EXP/train_devel.json.gz 
# Extracts the most frequent words
./bin/extract_info.py -wordfreq $EXP/train_devel.json.gz

# exctracts relevant words, based on TFIDF (1000 words)
./bin/extract_info.py -q $EXP/train_devel.json.gz -tfidf | awk '{print $1}' | head -1000 > $EXP/most-relevant-words.txt
cat $EXP/most-relevant-words.txt | head -2500 | awk '{print $1}' > data/most-relevant-words.txt

# Extracting the reference
./bin/extract_info.py -q $EXP/devel.json.gz -tag > $EXP/devel.ref
./bin/extract_info.py -q $EXP/test.json.gz -tag > $EXP/test.ref

# train and evaluate
# ---------------------------------------------------------------------------------------------------
./bin/topic_fingerpr.py -k=4000 $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 6378/17910, ACCURACY: 0.356114 (K=500)
# Correct 6538/17910, ACCURACY: 0.365047 (K=750)
# Correct 6629/17910, ACCURACY: 0.370128 (K=1000)
# Correct 6947/17910, ACCURACY: 0.387884 (K=1500)
# Correct 7078/17910, ACCURACY: 0.395198 (K=2000)
# Correct 7162/17910, ACCURACY: 0.399888 (K=2500)
# Correct 7200/17910, ACCURACY: 0.402010 (K=3000)
# Correct 7236/17910, ACCURACY: 0.404020 (K=4000)

# Correct 5280/17910, ACCURACY: 0.294807 (K=120, FP2: FP also for companies, PARETO)

# Correct 7223/17910, ACCURACY: 0.403294 (K=4000, FP2: FP also for companies, PARETO, MAX(i,j) )


./bin/topic_tfidf.py -f=10 $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 6030/17910, ACCURACY: 0.336683 (minfreq=18)
# Correct 6090/17910, ACCURACY: 0.340034 (minfreq=10)


# Criar arff
# ---------------------------------------------------------------------------------------------------
./bin/createarff.py $EXP/train_devel.json.gz | gzip > $EXP/train_devel.arff.gz
./bin/createarff.py $EXP/train.json.gz | gzip > $EXP/train.arff.gz
./bin/createarff.py $EXP/train.arff.gz $EXP/test.json.gz | gzip > $EXP/test.arff.gz
./bin/createarff.py $EXP/train.arff.gz $EXP/devel.json.gz | gzip > $EXP/devel.arff.gz

CLASSPATH=/Applications/Misc/weka-3-6-11
CLASSPATH=/afs/l2f/home/fmmb/usr/src/weka-3-6-9

# fast methods
CLASSIFIER=(weka.classifiers.rules.ZeroR)
CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomial)
CLASSIFIER=(weka.classifiers.bayes.NaiveBayesMultinomialUpdateable)

CLASSIFIER=(weka.classifiers.bayes.NaiveBayesUpdateable) 

CLASSIFIER=(weka.classifiers.functions.SMO -C 1.0 -L 0.0010 -P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0")
CLASSIFIER=(weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W 0.0)
CLASSIFIER=(weka.classifiers.functions.Logistic -R 1.0E-8 -M -1)
CLASSIFIER=(weka.classifiers.bayes.NaiveBayes)
# Other possible
CLASSIFIER=(weka.classifiers.trees.SimpleCart -S 1 -M 2.0 -N 5 -C 1.0)
CLASSIFIER=(weka.classifiers.functions.MultilayerPerceptron -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a)
CLASSIFIER=(weka.classifiers.trees.J48 -C 0.25 -M 2)
CLASSIFIER=(weka.classifiers.lazy.KStar -B 20 -M a)

java -Xmx6g -classpath $CLASSPATH/weka.jar $CLASSIFIER -i -k -t $EXP/train.arff.gz -T $EXP/devel.arff.gz > $EXP/devel.$(echo $CLASSIFIER[1] | sed -E 's/^[^ ]*\.//').txt

# PAra usar o weka com mais memoria
java -Xmx6g -jar $CLASSPATH/weka.jar

# OLD VALUES
# ZeroR: 29.0727
# Naive Bayes: 36.8421 ACCuracy
# Naive Bayes Multinomial: 40.3509 %
# SimpleLogistic: 38.3459
# J48: 31.4536
# SMO: 36.9674
# KStar: 32.3308


