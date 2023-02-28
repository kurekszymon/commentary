import inspect
from time import time
from collections import defaultdict

import torch
import pandas as pd
import numpy as np
from transformers import get_linear_schedule_with_warmup
from torch.utils.data import DataLoader

import _GPReviewDataset


def get_predictions(model, data_loader):
    model = model.eval()

    review_texts = []
    predictions = []
    prediction_probs = []
    real_values = []
    with torch.no_grad():
        for d in data_loader:
            outputs = model(
                input_ids=d["input_ids"], attention_mask=d["attention_mask"]
            )
            _, preds = torch.max(outputs, dim=1)
            review_texts.extend(d["review_text"])
            predictions.extend(preds)
            prediction_probs.extend(outputs)
            real_values.extend(d["targets"])

    predictions = torch.stack(predictions)
    prediction_probs = torch.stack(prediction_probs)
    real_values = torch.stack(real_values)

    return review_texts, predictions, prediction_probs, real_values


def train_model(epochs, model, train_data_loader, val_data_loader, df_train, df_val):
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    total_steps = len(train_data_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=total_steps
    )
    loss_fn = torch.nn.CrossEntropyLoss()
    history = defaultdict(list)
    best_accuracy = 0
    start = time()
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        print("-" * 10)
        train_loss, train_acc = train_epoch(
            model, train_data_loader, loss_fn, optimizer, scheduler, len(df_train)
        )
        print(f"Train loss {train_loss} accuracy {train_acc}")
        val_loss, val_acc = eval_model(model, val_data_loader, loss_fn, len(df_val))
        print(f"Val   loss {val_loss} accuracy {val_acc}")
        history["train_acc"].append(train_acc)
        history["train_loss"].append(train_loss)
        history["val_acc"].append(val_acc)
        history["val_loss"].append(val_loss)
        if val_acc > best_accuracy:
            torch.save(model.state_dict(), "models/actual_training_model.bin")
            best_accuracy = val_acc
    end = time()
    elapsed = f"{(end - start) / 60} minutes {end - start % 60} "
    print("Time elapsed", elapsed, end - start)


def train_epoch(model, data_loader, loss_fn, optimizer, scheduler, n_examples):
    model = model.train()
    losses = []
    correct_predictions = 0
    for d in data_loader:
        outputs = model(input_ids=d["input_ids"], attention_mask=d["attention_mask"])
        _, preds = torch.max(outputs, dim=1)
        loss = loss_fn(outputs, d["targets"])
        correct_predictions += torch.sum(preds == d["targets"])
        losses.append(loss.item())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
    return correct_predictions.double() / n_examples, np.mean(losses)


def eval_model(model, data_loader, loss_fn, n_examples):
    model = model.eval()
    losses = []
    correct_predictions = 0
    with torch.no_grad():
        for d in data_loader:
            outputs = model(
                input_ids=d["input_ids"], attention_mask=d["attention_mask"]
            )
            _, preds = torch.max(outputs, dim=1)
            loss = loss_fn(outputs, d["targets"])
            correct_predictions += torch.sum(preds == d["targets"])
            losses.append(loss.item())
    return correct_predictions.double() / n_examples, np.mean(losses)


def create_data_loader(df: pd.DataFrame, tokenizer, max_len: int, batch_size: int):
    ds = _GPReviewDataset.GPReviewDataset(
        reviews=df.review.to_numpy(),
        targets=df.sentiment.to_numpy(),
        max_len=max_len,
        tokenizer=tokenizer,
    )

    # https://github.com/pytorch/pytorch/issues/8976
    return DataLoader(ds, batch_size=batch_size, num_workers=0)


def convert_txt_to_pandas_df(path: str):
    suffix = ".txt"
    if suffix not in path:
        path = path + suffix
    dict = {"review": [], "score": []}
    with open(path) as f:
        for line in f.readlines():
            review, score = line.split("__label__z_")

            score = score.strip()
            score = score.replace("\n", "")
            score = map_score(score)

            dict["review"].append(review)
            dict["score"].append(score)
    df = pd.DataFrame.from_dict(dict)
    return df


def map_score(score):
    # https://clarin-pl.eu/dspace/handle/11321/700 thanks
    scores = {
        "wish": "0",
        "minus_m": "1",  # 1 - strong negative
        "minus_s": "2",  # 2 - weak negative
        "zero": "3",  # 3 - neutral
        "plus_s": "4",  # 4 - weak positive
        "plus_m": "5",  # 5 - strong positive
        "amb": np.nan,  # ambigous, filter out
    }
    return scores[score]


def to_sentiment(rating):
    rating = int(rating)
    if rating == 0:
        return 3  # last index in classnames array
    if rating <= 2:
        return 0
    elif rating == 3:
        return 1
    else:
        return 2


def print_lines(n=1):
    return print("\n" * n)


# upgrade to use args not list
def print_seperately(args=None):
    _, callstack = inspect.stack()
    _, file, line, *other = callstack
    file = file.split("/")[-1]

    print_lines()
    print(f"---{file}, line: {line}---")

    if isinstance(args, str):
        args = [args]

    for x in args:
        print(x, "\n")

    print("---End---")
    print_lines()
