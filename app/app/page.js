'use client'

import React, {useState} from "react";
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

    const getTour = () => {
        //TODO
        }

    
    return(
        <>
        {(state === 0) && <Home parentCallback={ (v) => enter(v) }/>}
        {(state === 1) && <New parentCallback={ (v) => handleClick(v) }/>}
        {(state === 2) && <Tour tour={tour} parentCallback={ (v) => handleClick(v) }/>}
        </>
    );
}
