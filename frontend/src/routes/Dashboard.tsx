import "./Dashboard.css";
import { useEffect, useState } from "react";
import { Cell, Legend, Pie, PieChart } from "recharts";
import { YoutubeEmbed, Table, Loader } from "../components";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import axios from "axios";
import { useNavigate, useParams } from "react-router";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";
import { Header } from "../components/Header";
import { Routes } from "../enums/routes";

enum Sentiment {
  NEUTRAL = "neutral",
  NEGATIVE = "negative",
  POSITIVE = "positive",
}
type Ratio = {
  sentiment: Sentiment;
  value: number;
};

type Comment = {
  sentiment: Sentiment;
  text: string;
};

const COLORS = { neutral: "#0088FE", positive: "#00c49f", negative: "#e32636" };

export const DashboardPage = () => {
  // TODO useReducer?
  const [data, setData] = useState<Ratio[]>([]);
  const [filteredData, setFilteredData] = useState<Ratio[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [noOfNewComments, setNoOfNewComments] = useState<number>();
  const [filteredComments, setFilteredComments] = useState<Comment[]>([]);
  const [isModalOpen, setModalOpen] = useState<boolean>(false);
  const { videoId } = useParams();
  const navigate = useNavigate();

  const [dimensions, setDimensions] = useState({
    height: window.innerHeight,
    width: window.innerWidth,
  });

  const isMobile = dimensions.width > dimensions.height;
  useEffect(() => {
    function handleResize() {
      setDimensions({
        height: window.innerHeight,
        width: window.innerWidth,
      });
    }

    window.addEventListener("resize", handleResize);
  }, []);

  const clearState = () => {
    setData([]);
    setFilteredData([]);
    setComments([]);
    setFilteredComments([]);
  };

  const navigateHome = () => navigate(Routes.HOME);

  const fetchAnalysis = async () => {
    // TODO move to utils?
    const res = await axios
      .get(
        `http://${import.meta.env.VITE_SERVER_URL}:5003/youtube/${videoId}/20`
      )
      .catch((e) => {
        return e;
      });

    return res;
  };

  function filterBySentiment<T extends Ratio | Comment>(
    data: T[],
    sentiment: Sentiment
  ): T[] {
    return data.filter((item: T) => item.sentiment === sentiment);
  }

  useEffect(() => {
    if (!videoId || data.length > 0) {
      return;
    }

    fetchAnalysis().then(({ data }) => {
      // {
      //   "comment": {
      //     "author": {
      //       "channel": "http://www.youtube.com/channel/UCH-syFvxNpUB13Qve4-4liA",
      //       "name": "ojwojtek"
      //     },
      //     "likes": 143,
      //     "publishedAt": "2022-12-29T13:52:13Z",
      //     "text": "Odcinki codziennie o 16 a ka\u017cda subskrypcja i follow na <a href=\"http://instagram.com/ojwojtek\">instagram.com/ojwojtek</a> to +10gr na <a href=\"http://zrzutka.pl/podarujwakacje\">zrzutka.pl/podarujwakacje</a> Moje zak\u0142ady z Japonii znajdziecie na stronie BETFAN w zak\u0142adce: rozrywka! Oferta tylko przez pierwsze 3 dni serii."
      //   },
      //   "sentiment": "neutral"
      // },
      const { comments, ratio } = data;
      // if (data.hasOwnProperty("no_of_new_comments")) {
      //   setModalOpen(true);
      //   setNoOfNewComments(data.no_of_new_comments ?? 0);
      // }

      const _ratio = Object.values(Sentiment)
        .map((sentiment) => ({
          sentiment,
          value: ratio?.[sentiment],
        }))
        .filter((review) => Boolean(review.value));

      setData(_ratio);
      setComments(comments);
    });
    return () => {
      clearState();
    };
  }, [videoId]);

  if (!videoId) {
    return <p>Provide valid youtube video id</p>;
  }

  return (
    <>
      <Header />
      <main
        className="dashboard"
        style={{
          flexDirection: !isMobile ? "column-reverse" : "row",
          justifyContent: !isMobile ? "flex-end" : "space-around",
        }}
      >
        {/* TODO move Dialog to external commponents */}
        <Dialog
          open={isModalOpen}
          onClose={() => setModalOpen(false)}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle>
            {"Use cached analysis? - do nothing right now :)"}
          </DialogTitle>
          <DialogContent>
            <DialogContentText>
              You have {noOfNewComments} new comments under this video, do you
              want to have cached version or do you want to perform full new
              analysis (will take more time)?
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setModalOpen(false)} autoFocus>
              Use cached
            </Button>
            <Button onClick={() => setModalOpen(false)}>Full analysis</Button>
          </DialogActions>
        </Dialog>
        <section
          className="dashboard__table"
          style={{
            alignItems: `${!comments.length ? "center" : ""}`,
            width: isMobile ? "50%" : "100%",
          }}
        >
          {!comments.length ? (
            <Loader visible height={480} width={120} />
          ) : (
            <Table
              data={filteredComments.length ? filteredComments : comments}
            />
          )}
        </section>

        <section
          className="dashboard__sidebar"
          style={{
            width: isMobile ? "20%" : "100%",
          }}
        >
          {!comments.length ? (
            <Loader visible height={250} />
          ) : (
            <div className="dashboard__sidebar--chart-area">
              <PieChart width={250} height={250}>
                <Pie
                  data={filteredData.length ? filteredData : data}
                  dataKey="value"
                  nameKey="sentiment"
                  outerRadius={50}
                  label
                >
                  {data.map(({ sentiment }, index) => (
                    <Cell
                      style={{ cursor: "pointer" }}
                      onClick={() => {
                        if (filteredData.length || filteredComments.length) {
                          return;
                        }

                        const _data = filterBySentiment(data, sentiment);
                        const _comments = filterBySentiment(
                          comments,
                          sentiment
                        );

                        setFilteredData(_data);
                        setFilteredComments(_comments);
                      }}
                      fill={COLORS[sentiment]}
                      key={index}
                    />
                  ))}
                </Pie>
                <Legend verticalAlign="top" height={48} />
              </PieChart>
              <Button
                variant="outlined"
                disabled={!filteredComments.length}
                onClick={() => {
                  setFilteredComments([]);
                  setFilteredData([]);
                }}
              >
                Clear selection
              </Button>
            </div>
          )}

          <div className="dashboard__sidebar--embed-area">
            <Button onClick={navigateHome}>
              <ChevronLeftIcon sx={{ verticalAlign: "sub" }} />
              Analyze new video
            </Button>
            <YoutubeEmbed embedId={videoId} />
          </div>
        </section>
      </main>
    </>
  );
};
