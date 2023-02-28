from time import time
import torch
from transformers import BertTokenizer

import consts

tokenizer = BertTokenizer.from_pretrained(consts.MODEL)
model = consts.SentimentClassifier(len(consts.CLASS_NAMES))
model.load_state_dict(torch.load("models/actual_training_model.bin"))


def eval_sentiment(comment):
    encoded_review = tokenizer.encode_plus(
        comment["text"],
        add_special_tokens=True,
        return_token_type_ids=True,
        return_attention_mask=True,
        return_tensors="pt",
        padding=True,
    )

    input_ids = encoded_review["input_ids"]
    attention_mask = encoded_review["attention_mask"]

    output = model(input_ids, attention_mask)
    _, prediction = torch.max(output, dim=1)
    return {"comment": comment, "sentiment": consts.CLASS_NAMES[prediction[0]]}


def eval_sentiment_list(texts):
    result = []

    for text in texts:
        sentiment = eval_sentiment(text)
        result.append(sentiment)

    return result


# def eval_local_sentiment():
#     results = []
#     evals = 0
#     reading_lines_time_start = time()
#     with open("data/youtube-tagged.txt", "r") as f:
#         lines = f.readlines()
#         reading_lines_time_end = time()

#         print(f"reading file: {reading_lines_time_end - reading_lines_time_start}s")
#         for line in lines:
#             evaluate_time_start = time()
#             try:
#                 sentiment = eval_sentiment(line)
#                 results.append(sentiment)
#                 evaluate_time_end = time()
#                 evals += evaluate_time_end - evaluate_time_start
#             except:
#                 print(line)
#     print(results)
#     print(f"eval file: {evals}s")

#     for item in results:
#         with open(f'data/evaluated/{item["sentiment"]}.txt', "a") as f:
#             f.writelines(item["text"])

