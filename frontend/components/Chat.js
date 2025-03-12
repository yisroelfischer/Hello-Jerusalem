import { useState, useEffect  } from 'react';
import { GoogleGenerativeAI } from '@google/generative-ai'
import ChatBot, {Button} from 'react-chatbotify';


export default function Chat({context=null}){
    const [model, setModel] = useState(null);
    const hat = '/yossi/hat.png'
    const settings = {
        general:{
            primaryColor: '#D9A577',
            secondaryColor: '#F2E4D8',
            showFooter: false,
            fontFamily:'Arial',
            flowStartTrigger: 'ON_CHATBOT_INTERACT'
        },
        tooltip: {
            mode: "START",
            text: 'Any questions?'
        },
        chatHistory:{
            disabled: true,
        },
        chatButton: {
            icon: hat
        },
        header: {
            title: (<h1>Yossi</h1>),
            avatar: hat,
            buttons: [Button.CLOSE_CHAT_BUTTON]
        },
        botBubble: {
            avatar: hat
        }
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


    // Chat functionality
    const getResponse = async (params) => {
        if (!model){
            return Error('Setup failed')
        }
        let offset = 0;
        let text = '';
        const res = await model.generateContentStream(params.userInput);
        for await (const chunk of res.stream){
            text += chunk.text();
            for(let i = offset; i < text.length; i++){
                await params.streamMessage(text.slice(0, i + 1));
                await new Promise(resolve => setTimeout(resolve, 30));
            }
            offset += chunk.text().length;
            }
        await params.endStreamMessage();
        }

    const flow = {
        start: {
            message: 'What\'s up?',
            path : 'loop'
        },
        loop: {
            message: async (params) => {
                return await getResponse(params)
            },
            path: 'loop'
        }
    }

    return (
        <div className='chat'>
        <ChatBot id='Yossi' flow={flow} settings={settings}/>
        </div>
    )
    
}