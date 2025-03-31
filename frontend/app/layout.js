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
      </head>
      <body >
        {children}
      </body>
    </html>
  );
}
