# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to classify objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import picamera
import os
import sys

from PIL import Image
from tflite_runtime.interpreter import Interpreter


filePath = os.path.dirname(os.path.realpath(__file__))

dirName = "images"
imageDirPath = os.path.join(filePath, dirName)

modelName = "model.tflite"
modelDir = "models"
modelDirPath = os.path.join(filePath, modelDir)
modelPath = os.path.join(modelDirPath, modelName)

labelName = "labels.txt"
labelPath = os.path.join(modelDirPath, labelName)


def load_labels(path):
  with open(path, 'r') as f:
    return {i: line.strip() for i, line in enumerate(f.readlines())}


def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]


def dryDetection(imageName):
  global results
  
  labels = load_labels(labelPath)
  interpreter = Interpreter(modelPath)
  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']

  imagePath = os.path.join(imageDirPath, imageName)
  image = Image.open(open(imagePath, 'rb')).convert('RGB').resize((width, height),
                                                     Image.ANTIALIAS)
  results = classify_image(interpreter, image)
  label_id = results[0][0]

  print(labels[label_id])
  return labels[label_id]
      

if __name__ == '__main__':
  if len(sys.argv) > 1:
   dryDetection(sys.argv[1])
  else:
   dryDetection()
