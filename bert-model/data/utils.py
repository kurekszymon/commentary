import pandas as pd


def check_untagged_lines():
    with open("data/check.txt") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "__label__" not in line:
                print(i + 1, "-", line)


def check_scores_distribution():
    with open("data/check.txt") as f:
        lines = f.readlines()
        dic = {"text": [], "scores": []}
        for i, line in enumerate(lines):
            de = line.strip().split("__label__z_")
            dic["text"].append(de[0])
            if len(de[0]) == len(de[0].strip()):
                print("Missing space or else:", i + 1)
            dic["scores"].append(de[1])
        df = pd.DataFrame.from_dict(dic)
        print(df["scores"].value_counts())


def check_coverage():
    with open("data/check.txt") as check:
        check_lines = len(check.readlines())
        with open("data/youtube-tagged.txt") as tagged:
            tagged_lines = len(tagged.readlines())
            cov = round(check_lines / tagged_lines * 100, 2)
            print(
                "\n",
                f"coverage: {cov}%",
                "\n",
                f"lines tagged and checked: {check_lines}",
                "\n",
                f"lines overall: {tagged_lines}",
            )


check_scores_distribution()
check_untagged_lines()
check_coverage()
