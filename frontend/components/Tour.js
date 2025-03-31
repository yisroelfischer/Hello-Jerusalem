import React, { useEffect, useState } from "react";
import Player from "./Player";
import Chat from "./Chat";
import TourMenu from "./TourMenu";

export default function Tour({
  setState,
  tour,
  tourIndex,
  setTourIndex,
  toursLength,
  children,
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [pathInfo, setPathInfo] = useState(null);
  const [siteInfo, setSiteInfo] = useState(null);
  const [currentType, setCurrentType] = useState("image");
  const [buttonText, setButtonText] = useState('Continue')

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
    document.activeElement.blur();
  };

  useEffect(() => {
    const setInfo = async () => {
      console.log("useEffect");
      const info = await getInfo();
      if (!info) {
        throw new Error(`No response recieved`);
      }
      console.log("setting info: ", info);
      if (info.image) {
        setCurrentType("site");
        setSiteInfo(`sites/${info.name}.jpg`);
      } else if (info.path) {
        setCurrentType("path");
        setPathInfo(info.path);
      }
    };
    setInfo();
  }, [currentIndex, tour]);

  return (
    <>
      {currentType === "site" && (
        <img className="site-image" src={siteInfo} alt="Site preview" />
      )}
      {currentType === "path" && (
        <Player info={pathInfo} setCurrentIndex={setCurrentIndex} />
      )}
      <TourMenu
        className="tour-menu"
        handleClick={handleClick}
        isLastSite={isLastSite}
        isLastTour={isLastTour}
      >
        <Chat className="tour-chat" />
      </TourMenu>
    </>
  );
}
