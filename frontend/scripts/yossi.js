import { GoogleGenerativeAI } from '@google/generative-ai'

const instruction  = `You are a tour guide for 'Hello, Jerusalem', a web app for taking 
        virtual walking tours of Jerusalem. Your name is Yossi. You are knowledgeable, friendly,
        and funny, with a stereotypically Israeli demeanor`;
const modelName = "gemini-2.0-flash";
const key = "AIzaSyCPD6QldeSLruUWN_sEJ4WjetG843Nw2a8"

async function getResponse(prompt){
    const genAI = new GoogleGenerativeAI(key);
    const model = genAI.getGenerativeModel({
        model:  modelName ,
        systemInstruction: instruction
    });

    let response = null;
    try{
        if (!prompt){
            console.error('missing prompt');
            return 'Something went wrong'
        }
        response = await model.generateContent(prompt);
        if (!response.response.text){
            console.log('Hi, there')
            throw new Error(`Error. Status: ${response.status}`);
        } 
        const text = response.response.text();
        return text;
        }
    catch(error){
        console.error('Error', error)
        return 'Error'
    }
}

export {getResponse}