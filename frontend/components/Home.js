import Guide from './Guide'

function Home({inProgress, parentCallback}) {
    
    const handleClick = (e)=> parentCallback(Number(e.target.dataset.value));
    const menuOptions = [
        {value:  0, label: 'Begin a new tour'},
        {value: 1, label: 'Continue an existing tour'}
    ]

    return (
        <>
        <Guide defaultPrompt='Welcome the user to the site in a few paragraphs'/>
        <div className="menu">
        {menuOptions.map((o)=> (<div className="button menu-button" 
                                         onClick={ (e)=> handleClick(e) } 
                                         data-value={o.value} 
                                         key={o.value}>
                                      {o.label}
                                    </div>))}
        </div>
        {(inProgress === true) && <div className="button" onClick={handleClick} value={'continue'}>
          Log in to continue a saved tour
    </div>}
        </> 
    )
}

export default Home;