# FB-tCNN for SSVEP
Here are the codes of the tCNN and FB-tCNN in the paper "Filter Bank Convolutional Neural Network for Short Time-Window Steady-State Visual Evoked Potential Classification" (DOI: 10.1109/TNSRE.2021.3132162). We will work on the codes as soon as possible.
## What you need to do
1. Download the code.
2. Download the public dataset ：https://academic.oup.com/gigascience/article/8/5/giz002/5304369 .
3. Create a model folder to save the model.
4. Change the data and model folder paths in train and test files to your data and model folder paths.
## The related version information
1. Python == 3.7.0
2. Keras-gpu == 2.3.1
3. tensorflow-gpu == 2.1.0
4. scipy == 1.5.2
5. numpy == 1.19.2
## Training FB-tCNN for your own dataset
1. You need to design the new filter bank according to your dataset (Fundamental range of the SSVEP-EEG data). The filter bank details can refer to our paper. The number of the sub-filters in the codes may be changed according to your own dataset. 
2. The frequency of the target should be changed according to your dataset.
