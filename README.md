# Introduction
This python package is a sample of using pandas
# How to run
I have provided setup.py and you can install by running the following command from the folder containing this readme
```
pip install -e pandas_sample
```
Then you can run the demo from another python project like this:
```
# example use
from pandas_sample import demo_naive, demo_experimental
demo_naive()
demo_experimental()
```
# Warning - Malformed Data Set
You need to add your dataset to data folder. For dev purposes I used [this dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) but as of this writing it is malformed. The file movies_metadata.csv contains overview field, 3 of its records are in freeform text, not enclosed in quotes, lines - 19764, 29573, 35672. If you intend to use that dataset, you need to fix those malformed lines.

Pandas handles malformed data amazingly, but it still has unintended side effects

I did not add the fixed dataset to this project, because setup of LFS is outside the scope of this project

The goal of this project is experimenting with pandas. Sanitizing arbitrary malformed data is much larger topic and also outside the scope of this project
# How to run tests
From tests folder:
```
pytest tests.py
```