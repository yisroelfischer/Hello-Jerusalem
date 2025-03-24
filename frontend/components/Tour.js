import React, { useEffect, useState } from "react";
import Player from "./Player";

export default function Tour({
  setState,
  tour,
  tourIndex,
  setTourIndex,
  toursLength,
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [src, setSrc] = useState(null);
  const [currentType, setCurrentType] = useState("image");

  const getInfo = async () => {
    console.log("tour:", tour, "currentIndex", currentIndex);
    const { type, id } = tour[currentIndex];
    let url = "";
    switch (type) {
      case "site":
        url = `http://127.0.0.1:5000/get-site?site=${id}`;
        console.log(url);
        break;
      case "path":
        const { start, end } = tour[currentIndex];
        url = `http://127.0.0.1:5000/get-path?path=${start},${end}`;
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
      console.log("info:", info);
      return info;
    } catch (error) {
      console.error("getInfo failed");
      return null;
    }
  };

  const handleClick = () => {
    console.log("tour.length:", tour.length, "currentIndex:", currentIndex);
    if (currentIndex === tour.length - 1) {
      if (tourIndex === toursLength - 1) {
        setCurrentIndex(0);
        setTourIndex(0);
        setState(0);
      } else {
        setCurrentIndex(0);
        setTourIndex((prev) => prev + 1);
      }
    } else {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  useEffect(() => {
    const a = async () => {
      console.log("useEffect");
      const info = await getInfo();
      if (!info) {
        throw new Error(`No response recieved`);
      }
      console.log("setting info: ", info);
      if (info.image) {
        setCurrentType("site");
        setSrc(`sites/${info.name}.jpg`);
      } else if (info.path) {
        setCurrentType("path");
        setSrc(info.path.url);
      }
    };
    a();
  }, [currentIndex, tour]);

  return (
    <>
      {currentType === "site" && <img src={src} alt="Site preview" />}
      {currentType === "path" && <Player url={src} />}
      <button className="button" onClick={handleClick}>
        Next
      </button>
    </>
  );
}
