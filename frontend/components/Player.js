import { useState } from "react";
import YouTube from "react-youtube";

export default function Player({ info, setCurrentIndex }) {
  const [loading, setLoading] = useState(true);

  const opts = {
    playerVars: {
      origin: "http://localhost:3000",
      start: info.startTime,
      end: info.endTime,
      autoplay: 1,
    },
  };

  const onReady = (event) => {
    setLoading(false);
    const player = event.target;
    player.setPlaybackRate(1.5);
  };

  const onPlayerStateChange = (event) => {
    if (event.target.getPlayerState() === 0) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  return (
    <div className="player-container">
      {loading && (
        <div className="loader-container">
          <div className="loader" />
        </div>
      )}
      {
        <YouTube
          videoId={info.videoId}
          opts={opts}
          onReady={onReady}
          onStateChange={onPlayerStateChange}
        />
      }
    </div>
  );
}
