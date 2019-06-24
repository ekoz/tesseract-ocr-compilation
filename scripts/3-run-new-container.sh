#!/bin/bash

docker run -d -v /tmp/t4-res:/tmp/t4-res -p 4022:22 --name t4cmp tesseractshadow/tesseract4cmp
docker ps