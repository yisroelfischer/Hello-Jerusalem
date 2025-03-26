import React from "react";

export default function Home({ children }) {
  return (
    <div className="container">
      <div id="welcome-message">
        <h1>Shalom and welcome to Hello, Jerusalem!</h1>
        <p>
          Hey there! I'm Yossi, your digital tour guide and your ticket to the
          most incredible city on the planet. Jerusalem isn't just a
          destination—it's a living, breathing story that's been unfolding for
          thousands of years, and now you get to explore it without leaving your
          couch! Want to walk the ancient streets, feel the stone walls that
          have witnessed millennia of history, and discover hidden gems that
          even some locals don't know about? Just pick your spots, and I'll
          craft a tour so immersive, you'll practically smell the fresh pita and
          hear the bustling market sounds. Got questions? Just give me a shout
          in the chat bubble. I've got stories that'll make history come alive
          faster than you can say "l'chaim"!
        </p>
      </div>
      {React.Children.map(children, (child, index) => (
        <div key={index}>
          {child}
        </div>
      ))}
    </div>
  );
}
