import React, { useEffect, useState } from "react";
import Player from "./Player";

export default function Tour({ parentCallback, tour }) {
  console.log(tour);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [current, setCurrent] = useState(null);

  const getInfo = async () => {
    const next = tour[currentIndex];
    console.log(`next: ${next}`);
    let url = "";
    switch (next.type) {
      case "site":
        url = `http://127.0.0.1:5000/get-site?site=${next.id}`;
        break;
      case "path":
        url = `http://127.0.0.1:5000/get-path?path=${next.start}${next.end}`;
    }
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`);
      }
      const info = await response.json();
      if (info.error) {
        throw new Error(info.error);
      }
      return info;
    } catch (error) {
      console.error("getInfo failed");
      return null;
    }
  };

  const handleClick = () => {
    setCurrentIndex((prev) => prev + 1);
  };

  useEffect(() => {
    if (currentIndex > tour.length()){
        parentCallback(endTour)
    }
    const a = async () => {
      console.log("useEffect");
      const info = await getInfo();
      if (!info) {
        throw new Error(`No response recieved`);
      }
      setCurrent(info);
    };
    a();
  }, [currentIndex]);

  return (
    <>
      {current && current.type === "site" && <img src={current.image}></img>}
      {current && current.type === "path" && <Player url={current.url} />}
      <button onClick={handleClick}>Next</button>
    </>
  );
}
