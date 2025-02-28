function Home({inProgress, parentCallback}) {
    
    const handleClick = (e)=> parentCallback(Number(e.target.dataset.value));
    const menuOptions = [
        {value:  0, label: 'Begin a new tour'},
        {value: 1, label: 'Continue an existing tour'}
    ]

    return (
        <>
         <div className="square">
            <img className="logo" src="/logo.png"></img>
            <div className="menu">
            {menuOptions.map((o)=> (<div className="button menu-button" 
                                             onClick={ (e)=> handleClick(e) } 
                                             data-value={o.value} 
                                             key={o.value}>
                                          {o.label}
                                        </div>))}
            </div>
            {(inProgress === true) && <div className="button" onClick={handleClick} value={'continue'}>
              Continue your tour
        </div>}
         </div>
        </>
    )
}

export default Home;