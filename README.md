# TeamPtolemy
This Repo contains code for TeamPtolemy's solution to Map Georeferencing Challenge held by DARPA.





- [TeamPtolemy](#teamptolemy)
  - [Installation](#installation)
  - [Model Running](#model-running)
    - [Amazon OCR](#amazon-ocr)
    - [Pytesseract OCR](#pytesseract-ocr)
    - [Ensemble Georeferencing](#ensemble-georeferencing)
  

## Installation

In stall the required packages through `pip install`:
```
pip install -r requirements.txt
```





## Model Running
Go to the under directory `code`:
```
cd code/
```

The running command is as following:
```
python run.py --dataset DATASET --mode MODE --data
_size LABLE_SIZE [--pretrained_path PRETRAINED_PATH]
```
`DATASET` describes the dataset, which should be among `[wisdm,rwhar,hhar,ecg]`. `MODE` describes the running mode, which should be among `[pretrain,train,finetune]`. `LABLE_SIZE` describes the size of labels used in training stage, which should be among `[full,few]`. `PRETRAINED_PATH` is requried when `MODE=finetune`; it indicates the path to pretrained checkpoint to start with.



### Amazon OCR

To perform full-label training, set `MODE` to `train` and `LABLE_SIZE` to `full`. For example, the command of full-label training on dataset WISDM is:
```
python amazon/slice.py --tif_path TIF_PATH --s3_path S3_PATH
```

```
python amazon/run.py --tif_path TIF_PATH
```


### Pytesseract OCR

To perform self-superviesed pretraining, set `MODE` to `pretrain`. For example, the command of full-label training on dataset WISDM is:
```
python pytesseract/run.py --tif_path TIF_PATH
```


### Ensemble Georeferencing

```
python ensemble/get_ans.py --csv_path CSV_PATH --clue_path CLUE_PATH
```

```
python ensemble/aggre.py 
```
