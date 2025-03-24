import "./globals.css";

export const metadata = {
  title: "Hello, Jerusalem",
  description: "virtual tour app",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/yossi/hat.png"></link>
        <link rel="preconnect" href="https://fonts.googleapis.com"></link>
        <link href="https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet"></link>
      </head>
      <body >
        {children}
      </body>
    </html>
  );
}
