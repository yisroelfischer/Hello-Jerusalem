'use client'

import React, {useState, useEffect} from "react";
import Home from '../components/Home'
import New from '../components/New'
import Tour from '../components/Tour'
import './globals.css'

export default function App (){
    const [tourIndex, setTourIndex] = useState(0);
    const [tours, setTours]= useState(null);
    const [state, setState] = useState(0);

    const enter  = (v) => {
        v === 0 ? setState(1) : getTour();
    }

    const getTour = async (sites) => {
        try{
            const url = `http://127.0.0.1:5000/get-tour?sites=${sites}`
            const response = await fetch(url);
            if (!response.ok){
                throw new Error(`HTTP error. Status: ${response.status}`)
            }
            const res = await response.json()
            setTours(res)
        } catch (error) {
            console.error('getTour failed');
            return null
        }
        
        }

    const handleClick = async (v) => {
        if (state === 1){
            console.log(`setting tour: ${v}`);
            getTour(v);
        }
        if (state === 2){
            if (tourIndex === tours.length()){
                setState(0)
            }
            setTourIndex(prev => prev+1)
        }
    }

    useEffect(() => {
        if (tours){
            setState(2)
        }
    },[tours]);
    
    return(
        <main>
        {(state === 0) && <Home parentCallback={ (v) => enter(v) }/>}
        {(state === 1) && <New parentCallback={ (v) => handleClick(v) }/>}
        {(state === 2) && <Tour tour={tours[tourIndex]} parentCallback={ (v) => handleClick(v) }/>}
        </main>
    );
}
