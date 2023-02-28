import * as React from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
type props = { data: any[]; headers?: any[] };

export function StickyHeadTable({ data, headers }: props) {
  // const columns = headers
  //   ? headers
  //   : ;

  return (
    <Paper
      sx={{
        width: "100%",
        overflow: "hidden",
        height: "90vh",
        backgroundColor: "#FBFAF5",
      }}
    >
      <TableContainer sx={{ maxHeight: "100%" }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {["sentiment", "text", "author", "likes", "published"].map(
                (column, i) => (
                  <TableCell key={column + i} align={"center"}>
                    {column}
                  </TableCell>
                )
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, i) => {
              const { comment, sentiment } = row;
              //   /{
              //     "comment": {
              //         "author": {
              //             "channel": "http://www.youtube.com/channel/UCFBH3Bdhgh3_cCToEQsUp6Q",
              //             "name": "Gimper"
              //         },
              //         "likes": 226,
              //         "publishedAt": "2022-12-30T13:34:01Z",
              //         "text": "Osiągnij technologiczną potęgę! Pobierz Rise of Kingdoms na: <a href=\"https://bit.ly/RoK23-gimper\">https://bit.ly/RoK23-gimper</a> i użyj kodu RoKTechPow, aby otrzymać specjalne nagrody w grze!"
              //     },
              //     "sentiment": "neutral"
              // }
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={i}>
                  <TableCell>{sentiment}</TableCell>
                  <TableCell>{comment.text}</TableCell>
                  <TableCell
                    onClick={() => {
                      return window.open(comment.author.channel, "_blank");
                    }}
                  >
                    {comment.author.name}
                  </TableCell>
                  <TableCell>{comment.likes}</TableCell>
                  <TableCell>
                    {new Intl.DateTimeFormat("pl-PL", {
                      year: "numeric",
                      month: "numeric",
                      day: "numeric",
                      hour: "numeric",
                      minute: "numeric",
                      second: "numeric",
                      hour12: false,
                    }).format(new Date(comment.publishedAt))}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
