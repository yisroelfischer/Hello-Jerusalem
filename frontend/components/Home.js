import React from "react";

export default function Home({children}) {
  return (
  <div className="container">
    <div id="welcome-message">
      <h1>Welcome to Hello, Jerusalem!</h1>
      <p>
        I'm your virtual tour guide, Yossi.
        Here you can experience Jerusalem as if you were there in person! 
        To begin, choose the sites you'd like to visit, and I'll generate a custom tour just for
        you! If you've got any questions, just type them into the text bubble at the bottom
        of the screen
      </p>
    </div>
    {children}
    <div className="placeholder"/>
  </div>
    )
}
