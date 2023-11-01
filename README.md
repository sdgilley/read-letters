# read-letters

I created this project to transcribe & display letters my parents sent to each other.  I first scanned the letters, which were written in cursive and hard to read.  This project transcribes the letters, then adds them all into a document.

There are two major steps to this project:

1. Extract the text from scanned images
1. Create a document with image / text next to each other

## Prerequisites

* Create a [Computer Vision resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision) in the Azure portal to get your key and endpoint. After it deploys, click **Go to resource**.

    * You will need the key and endpoint from the resource you create to connect your application to the Computer Vision service. Add your key and endpoint as environment variables as shown below.
    * You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production. 

* Create the following environment variables to be accessed when you run the Python script:
    * `COMPUTER_VISION_ENDPOINT` - the endpoint you created from the OCR Quickstart
    * `COMPUTER_VISION_SUBSCRIPTION_KEY` - the key you created from the OCR Quickstart

* Install the following libraries for `read-letters.py`:

    ```console
    pip install --upgrade azure-cognitiveservices-vision-computervision
    pip install pillow
    pip install PyGithub  
    ```

* Install the following libraries for `create-doc.py`:

    ```console
    pip install python-docx
    pip install docx2pdf
    ```

## Extract text from images

First, run `read-letters.py` to read the text from the images. This creates a .txt file for each image file in the given directory.

You may want to then read the .txt files and fix any errors. For my parent's letters, it gets around 60% right, so it still needs some manual editing.

## Create a document

Once you have extracted text, run `create-doc.py` to create a document with the images and text next to each other. This script creates both a .docx and .pdf file with the images and text.

(Not much error checking here yet, so make sure each image has a corresponding .txt file.)

`create-doc.py` assumes the following format for each image:

mm-dd-yy-who-p-where.jpg (or .png) where:

* mm-dd-yy: Month, day, year
* who: Who the letter is from
* p: Page number
* where: Where the letter was sent from

For example: 01-11-54-dad-1-richmond.jpg

The script reads this information to form the heading for each image.  If you change the format of these files, change the script section that puts together a heading as well.

Using the date in the name helps get the display sorted in a reasonable fashion. If you have some other way you want to sort your images, use that in the name instead.  But then make sure to modify the heading variable in the script to reflect what the name means.  

This is the section in the script that parses the file name and creates the heading:

```python
            # split apart name to get the date, who, where, and page number.
            date = '/'.join(parts[:2])
            year = f"{century}{parts[2]}" # add century to year
            date = f"{date}/{year}"
            who = parts[3].capitalize()  
            p = parts[4]
            where = parts[5].capitalize() 
            # create a heading for this particular letter
            heading = f"From {who}, Postmarked {date} {where}, p {p}"
```
