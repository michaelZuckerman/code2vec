type=python
dataset_name=my_dataset
data_dir="/Users/michaelzuckerman/Desktop/Study/code2vec/data/my_dataset"
data=${data_dir}/${dataset_name}
test_data=${data_dir}/${dataset_name}.val.c2s
model_dir=models/${type}

mkdir -p ${model_dir}
set -e
echo --data ${data} --test ${test_data} --save_prefix ${model_dir}/model
python3 -u code2seq.py --data ${data} --test ${test_data} --save_prefix ${model_dir}/model
