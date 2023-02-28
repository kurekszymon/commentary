import torch
import pandas as pd
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import eda
from consts import MODEL, RANDOM_SEED, BATCH_SIZE, CLASS_NAMES
from utils import (
    convert_txt_to_pandas_df,
    create_data_loader,
    to_sentiment,
    train_model,
    get_predictions,
)
from _SentimentClassifier import SentimentClassifier

if __name__ == "__main__":
    df_youtube = convert_txt_to_pandas_df("data/check")
    df_reviews = convert_txt_to_pandas_df("data/all2.sentence.train")
    df = pd.concat([df_reviews, df_youtube])
    df = df.dropna()  # drops null values

    df["sentiment"] = df.score.apply(to_sentiment)
    print(df)
    tokenizer = BertTokenizer.from_pretrained(MODEL)
    eda.quick_eda(df, tokenizer)
    MAX_LEN = 100

    df_train, df_test = train_test_split(df, test_size=0.1, random_state=RANDOM_SEED)
    df_val, df_test = train_test_split(df_test, test_size=0.5, random_state=RANDOM_SEED)

    train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
    val_data_loader = create_data_loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE)
    test_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

    data = next(iter(train_data_loader))

    model = SentimentClassifier(len(CLASS_NAMES))

    EPOCHS = 1
    # train_model(
    #     epochs=EPOCHS,
    #     model=model,
    #     train_data_loader=train_data_loader,
    #     val_data_loader=val_data_loader,
    #     df_train=df_train,
    #     df_val=df_val,
    # )
    # Evaluation
    model = SentimentClassifier(len(CLASS_NAMES))
    model.load_state_dict(torch.load("models/actual_training_model.bin"))

    y_review_texts, y_pred, y_pred_probs, y_test = get_predictions(
        model, test_data_loader
    )

    print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))
