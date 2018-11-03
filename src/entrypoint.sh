#!/bin/sh

echo "########## Installing requirements from packages ##########"
cd packages
find -name "requirements.txt" | xargs -I{} pip3 install -r {} --user
cd ../
echo "##########   Finished installing requirements    ##########"
python3 system.py
