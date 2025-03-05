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
            const url = `http://127.0.0.1:3001/get-tour?sites=${sites}`
            const response = await fetch(url);
            if (!response.ok){
                throw new Error(`HTTP error. Status: ${response.status}`)
            }
            const tour = await response.json()
            setTour(tour)
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
    }

    useEffect(() => {
        if (tour){
            setState(2)
        }
    },[tour]);
    
    return(
        <div className="main">
        {(state === 0) && <Home parentCallback={ (v) => enter(v) }/>}
        {(state === 1) && <New parentCallback={ (v) => handleClick(v) }/>}
        {(state === 2) && <Tour tour={tour} parentCallback={ (v) => handleClick(v) }/>}
        </div>
    );
}
