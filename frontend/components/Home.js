
import { getResponse } from '../scripts/yossi.js';
import { useEffect, useState } from 'react';

function Home({inProgress, parentCallback}) {
    const [text, setText] = useState(null)
    const handleClick = (e)=> parentCallback(Number(e.target.dataset.value));
    const menuOptions = [
        {value:  0, label: 'Begin a new tour'},
        {value: 1, label: 'Log in to continue an existing tour'}
    ]

    const formatText = (res)=> {
        const txt = res.split("\n").map((par, i) => (<p key={i}>{par}</p>));
        console.log(txt);
        return txt
    }

    useEffect(()=>{ (async() => {
        const res = await getResponse(`Welcome the user to the site in a few paragraphs. Explain that 
            they can select the sites they want to visit and you'll set up a tour for them. Let  
            them know that they can chat with you at any time by clicking or tapping on the hat 
            icon.`);
            const txt = formatText(res);
            setText(txt)
        })();
    },[])

    return (
        <>
        {(text === null) && <img src='/yossi/hat.png' className='hat'></img>}
        {(text != null) && <div className='bubble left'>
                                <p className="chat-text">
                                    <img src='/yossi/hat.png' className='inner-hat'></img>
                                    {text}
                                </p>
                            </div>}
        
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