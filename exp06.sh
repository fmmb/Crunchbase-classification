EXP=exp06.41tags
mkdir -p $EXP

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
./bin/topic_fingerpr.py -k=4000 $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 7065/16072, ACCURACY: 0.439584 (K=4000)

# Correct 5217/16072, ACCURACY: 0.324602 (K=120, FP also for companies, PARETO) 47,516 total
# Correct 4911/16072, ACCURACY: 0.305562 (K=500, FP also for companies, PARETO)
# Correct 4823/16072, ACCURACY: 0.300087 (K=1000, FP also for companies, PARETO min(i,j) ) 59,212 total

# Correct 6491/16072, ACCURACY: 0.403870 (K=1000, FP also for companies, PARETO, max(i,j) ) 59,318 total
# Correct 6956/16072, ACCURACY: 0.432802 (K=2000, FP also for companies, PARETO, max(i,j) ) 59,771 total
# Correct 7069/16072, ACCURACY: 0.439833 (K=4000, FP also for companies, PARETO, max(i,j) ) 1:05,29 total
# Correct 6914/16072, ACCURACY: 0.430189 (K=5000)

./bin/topic_tfidf.py -f=10 $EXP/train.json.gz $EXP/devel.json.gz | ./bin/evaluate.py $EXP/devel.ref
# Correct 5684/16072, ACCURACY: 0.353659 (freqmin=10)
# Correct 5490/16072, ACCURACY: 0.341588 (fm=18)
# Correct 5654/16072, ACCURACY: 0.351792 (fm=5)
