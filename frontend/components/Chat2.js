import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import { useState, useRef, useEffect } from 'react'

export default function Chat({context=null}){
    const history = useRef([])
    const [response, setResponse] = useState('')

    const submitQuestion = (question)=>{
        history.current = [
            ...history.current, 
            {role: 'user', parts: [{text: question}]}
        ]
    }

    //Setup
    useEffect(()=>{
        const setup = async() =>{
        // Fetch API key
        const getKey = (await fetch('http://localhost:5000/gemini-api-key'));
        const key = await getKey.json();
        if(key.error){
            return 'Error'
            }
        
        // Initialize model
        const genAI =new GoogleGenerativeAI(key.key);
        const m = genAI.getGenerativeModel({
            model: "gemini-2.0-flash",
            systemInstruction: `You are a tour guide for 'Hello, Jerusalem', a web app for 
            taking virtual walking tours of Jerusalem. Your name is Yossi. You are 
            knowledgeable, friendly,and funny, with a stereotypically Israeli personality. ${context}`,
            });
        setModel(m)
        }
        setup();
    }, [])

    return(
        <>
        {response && <Response response={response}/>}
        <Input submitQuestion={submitQuestion}/>
        </>
    )
}

function Input({submitQuestion}){
    const handleSubmit = (e) => {
        e.preventDefault();
        const question = e.target[0].value;
        if (!question) return;
        submitQuestion(question);
        e.target.reset();
    }

    return (
        <form className="input" onSubmit={handleSubmit}> 
            <input type="text" placeholder="Ask Yossi anything"/>
            <button type="submit">
                <FontAwesomeIcon icon={faPaperPlane}/>
            </button>
        </form>
    )
}

function Response({response}){
    return (
        <div className="response">
            <p>{response}</p>
        </div>
    )
}

