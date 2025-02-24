import sampleData from '../app/sampleData'
import React,{ useState } from 'react'

function New({parentCallback}) {

    const [picked, setPicked] = useState([]);

    const handleSubmit = (e)=> parentCallback(picked);
    const handleChange = (e)=> {
        (e.target.checked) ? setPicked([...picked, e.target.value]) : setPicked(picked.filter(i => i != e.target.value));
    };

    const sites = sampleData.sites;

    return(
        <>  
        <form className="square">
            <a href="./"><img src="/logo.png" className="logo"></img></a>
            <p>Where would you like to go?</p>
            <div className='list'>
                {sites.map((site) => <>
                  <input type='checkbox' onChange={ handleChange } value={site.id} key={site.id}/>
                  <label>{site.name}</label></>)}
            </div>
            <button className='button' onClick={handleSubmit}>Begin tour</button>
        </form>
        </>
    )
}

export default New