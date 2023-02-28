import seaborn as sns
import pandas as pd
from consts import CLASS_NAMES
import matplotlib.pyplot as plt


def quick_eda(df: pd.DataFrame, tokenizer):
    ax = sns.countplot(x=df.sentiment)
    ax.set_xticklabels(CLASS_NAMES)
    plt.xlabel("review sentiment")

    print(df, df.info())

    token_lens = []
    for txt in df.review:
        tokens = tokenizer.encode(txt, max_length=512)
        token_lens.append(len(tokens))
    sns.displot(token_lens)
    plt.xlim([0, 1000])
    plt.xlabel("Token count")
    plt.show()
