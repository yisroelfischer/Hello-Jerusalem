
import { getResponse } from '../scripts/yossi.js';
import { useEffect, useState } from 'react';

function Home({inProgress, parentCallback}) {
    const handleClick = (e)=> parentCallback(Number(e.target.dataset.value));
    const menuOptions = [
        {value:  0, label: 'Begin a new tour'},
        {value: 1, label: 'Log in to continue an existing tour'}
    ]

    return (
       <>
       <h1>Welcome to Hello, Jerusalem!</h1>
       <h2>I'm your AI tour guide, Yossi. I'll be available to answer any questions you have on your trip. 
        Click Begin Tour to get started! </h2>
        <div className="menu">
        {menuOptions.map((o)=> (<button className="button menu-button" 
                                         onClick={ (e)=> handleClick(e) } 
                                         data-value={o.value} 
                                         key={o.value}>
                                      {o.label}
                                    </button>))}
        </div>
        {(inProgress === true) && <div className="button" onClick={handleClick} value={'continue'}>
          Continue your tour
        </div>}
        </> 
    )
}

export default Home;