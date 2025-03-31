import React from "react";

export default function Home({ children }) {
  return (
    <div className="container">
      <div className="container-item">
        <div id="welcome-message">
          <h1>Shalom!</h1>
          <h2>
            I'm Yossi, your virtual tour guide! Want to walk Jerusalem's ancient
            streets, feel the stone walls that have witnessed millennia of
            history? Just pick your spots, and I'll craft a tour so immersive,
            you'll practically smell the fresh pita and hear the bustling market
            sounds. Got questions? Just give me a shout in the chat bubble. I've
            got stories that'll make history come alive faster than you can say
            "l'chaim"!
          </h2>
        </div>
      </div>
      {React.Children.map(children, (child, index) => (
        <div className="container-item" id={child} key={index}>
          {child}
        </div>
      ))}
    </div>
  );
}
