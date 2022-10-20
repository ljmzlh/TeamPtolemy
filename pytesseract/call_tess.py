#Detects text in a document stored in an S3 bucket. Display polygon box around text and angled text 
import boto3
import io
from PIL import Image, ImageDraw
import pytesseract

def call_tess(rgb):
    options = "outputbase digits"
    ret = pytesseract.image_to_data(rgb, config=options,output_type='dict')
    return ret
    
if __name__ == "__main__":
    call_tess('GEO_0039_3.tif')

