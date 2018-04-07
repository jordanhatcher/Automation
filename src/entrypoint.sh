#!/bin/sh

echo "########## Installing requirements from packages ##########"
cd system/packages
find -name "requirements.txt" | xargs -I{} pip3 install -r {}
cd ../../
echo "##########   Finished installing requirements    ##########"
python3 main.py
