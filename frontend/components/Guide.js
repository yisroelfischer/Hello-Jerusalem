import { GoogleGenerativeAI } from '@google/generative-ai'
import { useState, useEffect  } from 'react';

export default function Guide({defaultPrompt}){
    const [prompt, setPrompt] = useState(null)
    const [content, setContent] = useState("Loading..")
    const genAI = new GoogleGenerativeAI("AIzaSyCPD6QldeSLruUWN_sEJ4WjetG843Nw2a8");
    const model = genAI.getGenerativeModel({
        model: "gemini-2.0-flash",
        systemInstruction: `You are a tour guide for 'Hello, Jerusalem', a web app for taking 
        virtual walking tours of Jerusalem. Your name is Yossi. You are knowledgeable, friendly,
        and funny, with a stereotypically Israeli demeanor` 
    });

    useEffect(()=> {
        async function getText() {
            let response = null;
            try{
                if (prompt){
                    console.log('getting response');
                    response = await model.generateContent(prompt);
                }
                else{
                    console.log('getting default response');
                    response = await model.generateContent(defaultPrompt);
                }
            
                 if (!response.response){
                    throw new Error(`Error. Status: ${response.status}`);
                } 
                setContent(response.response.text);
                }
            catch(error){
                console.error('Error', error)
                setContent('Error')
            }
        }
        getText()
        
    },[prompt])

    const handlePrompt = (e)=> {
        e.preventDefault();
        const userPrompt = e.target.value
        setPrompt(userPrompt)
    }

    return (<div className="chat">
                <div className="bubble left"> 
                    <div className="chat-text" ><img src='/Yossi/hat.png' className='inner-hat'></img>{ content }</div> 
                </div>
                <input type='text' onSubmit={ handlePrompt } className='bubble right'></input>
                
     </div>)
    
}