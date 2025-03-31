import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { useState, useRef, useEffect, useContext } from "react";
import { GoogleGenAI } from "@google/genai";

export default function Chat({ localContext = null }) {
  const history = useRef([]);
  const [response, setResponse] = useState("");

  const submitQuestion = async (question) => {
    setResponse("");
    const res = await getResponse(question);
    const text = res.split("");
    for (let i = 0; i < text.length; i++) {
      setTimeout(() => setResponse((prev) => prev + text[i]), 50);
    }

    console.log("response recieved");
    history.current.push(
      { role: "user", parts: [{ text: question }] },
      { role: "model", parts: [{ text: res }] }
    );
  };

  const getResponse = async (question) => {
    console.log("getResponse");
    // Fetch API key
    const getKey = await fetch("http://localhost:5000/gemini-api-key");
    const key = await getKey.json();
    if (key.error) {
      console.log(key.error);
      console.error("Error getting key");
      return;
    }

    // Initialize model
    const genAI = new GoogleGenAI({ apiKey: key.key });

    if (localContext) {
      context = context + localContext;
    }

    if (history.current) {
      console.log(history.current);
      const chat = genAI.chats.create({
        model: "gemini-2.0-flash",
        config: {
          systemInstruction: `You are a tour guide for 'Hello, Jerusalem', a web app 
    for taking virtual walking tours of Jerusalem. Your name is Yossi. You are knowledgeable, 
    friendly,and funny, with a stereotypically Israeli personality.`,
        },
        history: history.current,
      });
      const res = await chat.sendMessage({ message: question });
      return res.text;
    } else {
      const message = await genAI.model.generateContent({
        model: "gemini-2.0-flash",
        config: {
          systemInstruction: `You are a tour guide for 'Hello, Jerusalem', a web app 
    for taking virtual walking tours of Jerusalem. Your name is Yossi. You are knowledgeable, 
    friendly,and funny, with a stereotypically Israeli personality.`,
        },
        contents: question,
      });
      const res = await message;
      return res.text;
    }
  };

  return (
    <div className="chat">
      {response && <Response className="response" response={response} />}
      <Input className="input" submitQuestion={submitQuestion} />
    </div>
  );
}

function Input({ submitQuestion }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("input recieved");
    const question = e.target[0].value;
    if (!question) return;
    submitQuestion(question);
    e.target.reset();
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input type="text" className="input-field" autoFocus="true"/>
      <button className="send-button" type="submit">
        <FontAwesomeIcon className="plane-icon" icon={faPaperPlane} />
      </button>
    </form>
  );
}

function Response({ response }) {
  return (
    <div className="response">
      <p>{response}</p>
    </div>
  );
}
