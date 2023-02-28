import "./Home.css";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import TwitterIcon from "@mui/icons-material/Twitter";
import YoutubeIcon from "@mui/icons-material/YouTube";
import { ArrowForward } from "@mui/icons-material";
import { TextField, Tooltip, Button } from "@mui/material";
import { Routes } from "../enums/routes";
import { Header } from "../components/Header";

export function HomePage() {
  const [isValidLink, setIsValidLink] = useState<boolean>(true);
  const [link, setLink] = useState<string>("");
  const [videoId, setVideoId] = useState<string>("");
  const navigate = useNavigate();

  const parseVideoId = (link: string): string => {
    const rx =
      /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
    const videoId = link.match(rx)?.[1] ?? "";

    return videoId;
  };

  const onChange = (
    e: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>
  ): void => {
    // https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
    const link = e.currentTarget.value;
    setLink(link);

    const videoId = parseVideoId(link);
    if (videoId !== "") {
      setIsValidLink(true);
      setVideoId(videoId);
    }
  };

  const onClick = () => {
    return navigate(`${Routes.YOUTUBE}/${videoId}`);
  };

  return (
    <div className="App--welcome">
      <Header />
      <div className="source-link">
        <div className="source-link__socials">
          <YoutubeIcon
            sx={{ fontSize: 64 }}
            style={{ borderBottom: "3px solid white" }}
          />
          <Tooltip
            title={<h1 style={{ fontSize: "14px" }}>Available soon.</h1>}
            placement="top"
          >
            <TwitterIcon
              sx={{ fontSize: 64 }}
              style={{ cursor: "not-allowed" }}
            />
          </Tooltip>
        </div>

        <TextField
          autoFocus
          error={!isValidLink}
          label="Video Link"
          placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
          className="source-link__input"
          value={link}
          onChange={onChange}
          focused={true}
          inputProps={{
            style: {
              color: "white",
            },
          }}
        />
        <Button
          className="source-link__button"
          variant={"contained"}
          disabled={!link}
        >
          <ArrowForward sx={{ fontSize: 48 }} onClick={onClick} />
        </Button>
      </div>
    </div>
  );
}
