'''
Read a scanned letter image and transcribe the text using Azure Cognitive Services Computer Vision API

This script accesses environment variables 
      COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_SUBSCRIPTION_KEY 
      see readme for details

 This script needs the following packages:
     pip install --upgrade azure-cognitiveservices-vision-computervision
     pip install pillow
     pip install PyGithub  

References:
    - SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision?view=azure-python
    - Documentaion: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/index
    - API: https://westus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/5d986960601faab4bf452005
'''

##### USER INPUT #####
img_path = "C:\\Git\\read-letters-data\\new"
######################

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

# Authenticate with key, endpoint from environment variables (assumes you've exported these)
# if not there, tell user to set it
try:    
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
except:
    print("Please set COMPUTER_VISION_ENDPOINT environment variable")
    sys.exit()

try:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
except:
    print("Please set COMPUTER_VISION_SUBSCRIPTION_KEY environment variable")
    sys.exit()
# *** End of Authenticate - you're now ready to run the script.

# Create the client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


'''
OCR: Read File using the Read API, extract text - local
This example extracts text from a local image, then writes the text to a .txt file with the same name
'''

num = 0
print(f"===== Reading images in {img_path} =====")
import os
# find the file names from the local repo.
for path,dirs,files in os.walk(img_path):
    for file in files: 
        read_image_path = os.path.join(path,file)
        fn = file.split('.')[0]
        ext = file.split('.')[1]
        
        if ext in ['jpg', 'png']: # only process the image files
            write_fn = os.path.join(path,f"{fn}.txt") # name the text file with same name as image
            f = open(write_fn, 'w+') # open the text file for writing
            read_image = open(read_image_path, "rb")             # Open the image

            # Call API with image and raw response (allows you to get the operation location)
            read_response = computervision_client.read_in_stream(read_image, raw=True)
            # Get the operation location (URL with ID as last appendage)
            read_operation_location = read_response.headers["Operation-Location"]
            # Take the ID off and use to get results
            operation_id = read_operation_location.split("/")[-1]

            # Call the "GET" API and wait for the retrieval of the results
            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status.lower () not in ['notstarted', 'running']:
                    break
                print (f"*** Processing {file} ***")
                time.sleep(10)

            # write the results to the text file, line by line
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        f.write(line.text)
                        f.write('\n')
            print()
            num += 1

print(f"Finished processing {num} images")