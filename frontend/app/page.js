"use client";

import React, { useState, useEffect } from "react";
import Home from "../components/Home";
import Form from "../components/Form";
import Tour from "../components/Tour";
import "./globals.css";
import Chat from "@/components/Chat";

export default function App() {
  const [tourIndex, setTourIndex] = useState(0);
  const [tours, setTours] = useState(null);
  const [loading, setLoading] = useState(true);
  const [state, setState] = useState(0);


  const getTours = async (sites) => {
    try {
      const url = `http://localhost:5000/get-tours?sites=${sites}`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`);
      }
      const res = await response.json();
      if (res.error) {
        console.log(res.error);
        return null;
      }
      return res;
    } catch (error) {
      console.error("getTour failed");
      return null;
    }
  };

  const handleClick = async (v) => {
    if (state === 0) {
      try {
        console.log(`setting tour: ${v}`);
        const res = await getTours(v);
        if (!res || res.error) throw new Error("Error");
        console.log("res = ", res);
        setTours(res);
        setLoading(false);
        setState(1);
      } catch (error) {
        console.error("handleClick state 1 failed");
      }
    }
  };

  return (
    <main>
      {state === 0 && 
        <Home>
          <Form parentCallback={(v) => handleClick(v)} />
        </Home>}
      {state === 1 && tours && (
        <Tour
          tour={tours[tourIndex]}
          setState={setState}
          setTourIndex={setTourIndex}
          tourIndex={tourIndex}
          toursLength={tours.length}
        >
          <Chat />
        </Tour>
      )}
    </main>
  );
}
