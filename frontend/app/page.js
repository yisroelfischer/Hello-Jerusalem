'use client'

import React, {useState, useEffect} from "react";
import Home from '../components/Home'
import New from '../components/New'
import Tour from '../components/Tour'
import './globals.css'

export default function App (){
    const [tour, setTour] = useState(null);
    const [state, setState] = useState(0);

    const enter  = (v) => {
        console.log(v)
        v === 0 ? setState(1) : getTour();
    }

    const getTour = async (sites) => {
        try{
            const tour = await fetch('http://127.0.0.1:3001/getTour', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({sites})
            });
            if (!tour.ok){
                throw new Error(`HTTP error. Status: ${tour.status}`)
            }

            return tour.json()
        } catch (error) {
            console.error('getTour failed');
            return null
        }
        
        }

    const handleClick = async (v) => {
        if (state === 1){
            tourList = await getTour(v)
            if (tourList) {
                setTour(tourList)
            }
            else {
                console.error('null tour list')
            }
        }
    }

    useEffect(() => {
        if (tour){
            setState(2)
        }
    },[tour]);
    
    return(
        <>
        {(state === 0) && <Home parentCallback={ (v) => enter(v) }/>}
        {(state === 1) && <New parentCallback={ (v) => handleClick(v) }/>}
        {(state === 2) && <Tour tour={tour} parentCallback={ (v) => handleClick(v) }/>}
        </>
    );
}
