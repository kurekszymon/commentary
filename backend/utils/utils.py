import requests
import consts

from dotenv import dotenv_values

config = dotenv_values()


def eval_sentiment(content):
    response = requests.post(
        "http://model:5002/api/sentiment-analysis",
        json={"content": content},
    )

    if response.status_code == 200:
        return response.json()


def get_comments(video_id, maxResults=10, fetchAll=False):
    api_key = config["YT_API_KEY"]

    # Set the parameters for the API request
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": 100 if fetchAll is True else maxResults,
        "pageToken": "",
    }

    comments = []

    while True:
        response = requests.get(consts.YT["commentThreads"], params=params)
        if response.status_code == 200:
            comment_threads = response.json()
            for comment_thread in comment_threads["items"]:
                snippet = comment_thread["snippet"]["topLevelComment"]["snippet"]
                text = snippet["textDisplay"]
                likes = snippet["likeCount"]
                publishedAt = snippet["publishedAt"]
                author = {"name": snippet["authorDisplayName"], "channel": snippet["authorChannelUrl"]}

                comments.append({"text": text, "likes": likes, "author": author, "publishedAt": publishedAt})
        else:
            raise Exception("Error occured:", response.status_code)

        if fetchAll is True and "nextPageToken" in response.json():
            params["pageToken"] = response.json()["nextPageToken"]
        else:
            break
    return comments


def get_channel_info_by_video(video_id):
    api_key = config["YT_API_KEY"]

    response = requests.get(
        consts.YT["videos"], {"part": "snippet", "id": video_id, "key": api_key}
    )

    video = response.json()["items"][0]
    channel_id = video["snippet"]["channelId"]
    channel_title = video["snippet"]["channelTitle"]

    # Can be moved to different function, redundant here
    # c_response = requests.get(
    #     consts.YT["channels"], {"part": "snippet", "forUsername": channel_title, "key": api_key}
    # )
    # channel = c_response.json()["items"][0]
    # channel_custom_url = channel["snippet"]["customUrl"]

    return {"id": channel_id, "title": channel_title}


def fetch_data():
    sources = [
        {
            "creator": "Wersow",
            "videos": [
                "ZZBZsZ8gGxs",
                "f_CgSSP9aN4",
                "WpgLtIv1RaQ",
                "6U43aOLkY2I",
                "vU6kVevA5G4",
                "qw4wNus7giQ",
                "sLNqxSjF8Eo",
                "kK_49sbS89w",
                "RCk44jmqikw",
                "Q-Ttl-orFzc",
            ],
        },
        {
            "creator": "Gimper",
            "videos": [
                "HOVFdEdjZIA",
                "nsCMwedkvms",
                "BzHqJ3PwWks",
                "7cYJ5NzEzUc",
                "PxU5yKy8a8U",
                "qXfnHBvFsyA",
                "GwR0codhYsk",
                "O1Tyw1ZpYsI",
                "25314eWbMeo",
                "qgiS1juFFcM",
            ],
        },
        {
            "creator": "Revo",
            "videos": [
                "5VBk42gkHq0",
                "e9O3MutMn_s",
                "rwVh0fzWeE8",
                "hAUlhC_d_i0",
                "gmj69EWpVIM",
                "jWrG6a6_lA8",
                "yAaCxlEl_rM",
                "G774ZoXKvn0",
                "c-1tQ81qDx4",
                "eb6VIpqCVbU",
            ],
        },
        {
            "creator": "Friz",
            "videos": [
                "ASsAt822QGU",
                "7XAqNqjQ0A4",
                "TFHLDyVURQE",
                "598GIyZFAl8",
                "gmj69EWpVIM",
                "HzWPfKS73f8",
                "w7dmGyeHFJo",
                "wxBLVYmcLT4",
                "uIDX1YaAMkI",
                "sx8hMCvU-zY",
            ],
        },
        {
            "creator": "Fame",
            "videos": [
                "_ENL3aQpLrE",
                "L5HskUbAaDA",
                "xxOKm_Vfaq8",
                "BJum1uap1OQ",
                "OdKAxX4ueDU",
                "UQF2MRYz5Bg",
                "m6fOOW6hF2A",
                "R5LEjVxyysQ",
                "VRZ3korpeao",
                "ABYKCKsQ808",
            ],
        },
        {
            "creator": "Imponderabilia",
            "videos": [
                "y8DGGOjSioM",
                "rbjsSbHFHjM",
                "xQLLilkvP7o",
                "g0Yj_aYKGZ0",
                "jRRevcumg7Q",
                "4z0xL_8Rj4E",
                "arVvLshBv48",
                "oScJEUc13dg",
                "rJb7hz9MH70",
                "az63tPEgl0o",
            ],
        },
        {
            "creator": "G.F. Darwin",
            "videos": [
                "REmV_JIkcZU",
                "0WY51yAzans",
                "3XXuLeTFO74",
                "XjPxSIZU6qM",
                "cf7bvRTx-f4",
                "pr_HlSJ-elI",
                "ZdcRFpdae2s",
                "BoTcm_ARzAk",
                "wggzXLJe_BA",
                "OnVrKdbT5U4",
            ],
        },
        {
            "creator": "Graf",
            "videos": [
                "hzAVd2lIcNE",
                "9oPYe7JhKsw",
                "nmXxFHMf2P4",
                "_XwYrJzvj6k",
                "LEclLNqY1dM",
                "frMvkjIK0fw",
                "YXPcfkr0gMM",
                "5axZtqRT_bE",
                "hE9LZj2LrUI",
                "N5ZRi4HhLGg",
            ],
        },
        {
            "creator": "Multi",
            "videos": [
                "e9NEejNX29A",
                "VdurwgKzRUU",
                "oM2DMGpdZSc",
                "cxWwK3j3GJE",
                "WAM7mTByHkg",
                "h_sjZngx0OU",
                "Cw2Vm_P5h64",
                "wGUgWwhWIdQ",
                "6KiFoskypYs",
                "bPmyceahXZg",
            ],
        },
        {
            "creator": "ojwojtek",
            "videos": [
                "wNZqnTXgPBQ",
                "Vp3UP-qPw1k",
                "LJPjXKDMdQg",
                "NIf_d61mEhw",
                "i2_f9cyU5bE",
                "zpTTl0cxVGg",
                "8NYtktBPD1g",
                "qjA1ws-v1vU",
                "WGBMMkKQ0uU",
                "g8EBvmaB7_w",
            ],
        },
    ]

    for source in sources:
        print(f"Creator - {source['creator']}")
        for video in source["videos"]:
            print(f"Video - {video}")
            with open("data/youtube-untagged.txt", "a") as f:
                comments = get_comments(video, fetchAll=True)
                for comment in comments:
                    f.writelines(comment + "\n")
