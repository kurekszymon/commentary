import fs from "fs";

const file = process.argv[2];
const [name, extension] = file.split(".");

if (extension !== "txt") {
  throw Error("Hey, use txt file.");
}

const contents = fs.readFileSync(file, "utf-8").split("\n");

const jsonified = JSON.stringify(
  contents
    .map((text) => ({ text }))
    .filter(({ text }) => Boolean(text))
    .concat({ text: "EOF" })
);

fs.writeFileSync(name + ".json", jsonified, { encoding: "utf-8" });
// console.log(contents, typeof contents);
