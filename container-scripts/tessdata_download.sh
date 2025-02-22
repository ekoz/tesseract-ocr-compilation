#!/bin/bash

# osd	Orientation and script detection
wget -O ${TESSDATA_PREFIX}/osd.traineddata https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata
# equ	Math / equation detection
wget -O ${TESSDATA_PREFIX}/equ.traineddata https://github.com/tesseract-ocr/tessdata/raw/3.04.00/equ.traineddata
# eng English
wget -O ${TESSDATA_PREFIX}/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/4.00/eng.traineddata
# other languages: https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
wget -O ${TESSDATA_PREFIX}/chi_sim.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/4.0.0/chi_sim.traineddata

wget -O ${TESSDATA_PREFIX}/chi_sim_vert.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/4.0.0/chi_sim_vert.traineddata
