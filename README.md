# code2vec
[Michael Zuckerman 066431222](michaelz@mail.tau.ac.il)
[David Shmuel 302782479](davidshmuel@mail.tau.ac.il)

Table of Contents
=================
  * [Requirements](#requirements)
  * [Quickstart](#quickstart)
  * [Configuration](#configuration)
  * [Releasing a trained mode](#releasing-a-trained-model)
  * [Extending to other languages](#extending-to-other-languages)
  * [Datasets](#datasets)
  * [Citation](#citation)

## Requirements
  * [python3](https://www.linuxbabe.com/ubuntu/install-python-3-6-ubuntu-16-04-16-10-17-04) 
  * TensorFlow 1.12 or newer ([install](https://www.tensorflow.org/install/install_linux)). To check TensorFlow version:
  * python ast
  * python pathlib

## Quickstart
### Step 0: Cloning this repository
```
git clone https://github.com/michaelZuckerman/code2vec.git
cd code2vec
```

### Step 1: Download and preprocessed dataset python dataset (40000 example)
```
mkdir data
cd data
curl https://www.dropbox.com/s/4q08j78f7hdbiob/python50starsplus.tar.gz?dl=0
tar -xvzf python50starsplus.tar.gz?dl=0
```
This will create a `50starsShuf/` sub-directory, containing the files that hold training, test and validation sets,
and a dict file for various dataset properties.

#### Creating and preprocessing a new Python dataset
To create and preprocess a new dataset:
  * Edit the file [preprocess.sh](preprocess.sh) using the instructions there, pointing it to the correct training, validation and test directories.
  * Run the preprocess.sh file:
> bash preprocess.sh


### Step 2: Training a model
You can either download an already trained model, or train a new model using a preprocessed dataset.

#### Downloading a trained model
We already trained a model for 60 epochs on the data that was preprocessed in the previous step.

#### Training a model from scratch
To train a model from scratch:
  * Edit the file [train.sh](train.sh) to point it to the right preprocessed data.
  * Run the [train.sh](train.sh) script:
```
bash train.sh
```

### Step 3: Evaluating a trained model
Suppose that iteration #1 is our chosen model, run:
```
python3 code2seq.py --load models_ttf/python_ftt/model_iter001 --test data_ttf/data/my_dataset/my_dataset.test.c2s
```

## Datasets
### Python
To download the python

  * [python](https://www.dropbox.com/s/4q08j78f7hdbiob/python50starsplus.tar.gz?dl=0)

