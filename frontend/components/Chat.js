import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { useState, useRef, useEffect } from "react";
import { GoogleGenAI } from "@google/genai";

export default function Chat({ localContext = null }) {
  const history = useRef([]);
  const [response, setResponse] = useState("");
  if (!localContext){
    
  }
  

  const submitQuestion = async (question) => {
    setResponse("");
    const chat = setup(history);
    if (!chat || !question.trim()) {
      console.error("Chat is not initialized yet.");
      return;
    }
    try {
      console.log("awaiting response");
      const res = await chat.sendMessage({
        message: question,
      });
      let text = await res;
      text = text.text.split("");
      for (let i = 0; i < text.length; i++) {
        setTimeout(() => setResponse((prev) => prev + text[i]), 50);
      }

      console.log("response recieved");
      history.current.push(
        { role: "user", parts: [{ text: question }] },
        { role: "model", parts: [{ text: res }] }
      );
    } catch (error) {
      console.log(`submitQuestion failed. Hi.  ${error}`);
      console.log(history);
    }
  };

  const setup = async(type, chatHistory=null) => {
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
    const newChat = genAI.chats.create({
      model: "gemini-2.0-flash",
      systemInstruction: context,
      history: chatHistory,
    });

    return newChat;
  }
    

  return (
    <>
      {response && <Response response={response} />}
      <Input submitQuestion={submitQuestion} />
    </>
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
    <form className="input" onSubmit={handleSubmit}>
      <input type="text" placeholder="Ask Yossi anything" />
      <button type="submit">
        <FontAwesomeIcon icon={faPaperPlane} />
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
