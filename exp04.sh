EXP=exp04.25tags
mkdir $EXP

# filters by selected tags
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
./bin/topic_fingerpr.py $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 6473/17910, ACCURACY: 0.361418 (K=500) 32,545 total
# Correct 5532/17910, ACCURACY: 0.308878 (K=120, FP2: FP also for companies, PARETO) 36,604 total

./bin/topic_tfidf.py $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 6169/17910, ACCURACY: 0.344444 (freqmin=18)


