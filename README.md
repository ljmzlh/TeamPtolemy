# TeamPtolemy
This Repo contains code for TeamPtolemy's solution to Map Georeferencing Challenge held by DARPA.





- [TeamPtolemy](#teamptolemy)
  - [Installation](#installation)
  - [Model Running](#model-running)
    - [Amazon OCR](#amazon-ocr)
    - [Pytesseract OCR](#pytesseract-ocr)
    - [Ensemble Georeferencing](#ensemble-georeferencing)
  

## Installation

Clone the repository and go to the root directory:
```
git clone https://github.com/ljmzlh/TeamPtolemy.git
cd TeamPtolemy/
```

Install the required packages through `pip install`:
```
pip install -r requirements.txt
```





## Model Running


### Amazon OCR

First, slice the images into smaller patches:
```
python amazon/slice.py --tif_path TIF_PATH --s3_path S3_PATH
```

Then, call Amazon Textract to perform OCR on the sliced smaller patches:
```
python amazon/run.py --tif_path TIF_PATH
```

`TIF_PATH` is the path to the directory containing tif files. `S3_PATH` is the path to your S3 storage bucket.

### Pytesseract OCR

Call Pytesseract OCR Model to perform OCR on the images:
```
python pytesseract/run.py --tif_path TIF_PATH
```
`TIF_PATH` is the path to the directory containing tif files.


### Ensemble Georeferencing

Ensemble and filter the coordinates captured by all the OCR models, build coordinate system and generate answers for target points:
```
python ensemble/get_ans.py --csv_path CSV_PATH --clue_path CLUE_PATH
```

Aggregate all the answers into one CSV file:
```
python ensemble/aggre.py 
```
`CSV_PATH` is the path to the directory containing target CSV files.
`CLUE_PATH` is the path to the directory containing clue CSV files.
