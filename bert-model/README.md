# Engaged Creator 

Project based on Flask and Transformers library to train model. 
I used Bert Model (pretrained `kleczek/bert-base-polish-cased-v1`), trained further with my own datasets, as it was in my opinion best suited for the case like this. 

Using pyenv, as tensorflow doesn't have stable version for python version > 3.10.9

## Training Model 

To train model run `python3 training/train_model.py`

### TODO
 - Move training data to console argument
 - Clean code with imports and stuff 

## Running API 

To start API run `python3 app.py`

### TODO 
- add db, store creators id -> videos -> sentiment analysis 
- add parameter `use-cached` to look up db/store new value for vid



should cite  https://clarin-pl.eu/dspace/handle/11321/700
@InProceedings{Kocon2019,
Title = {{Multi-level analysis and recognition of the text sentiment on the example of consumer opinions}},
Author = {Koco{\'n}, Jan and Zaśko-Zielińska, Monika and Miłkowski, Piotr},
Booktitle = {Proceedings of the International Conference Recent Advances in Natural Language Processing, RANLP 2019},
Year = {2019},
}
