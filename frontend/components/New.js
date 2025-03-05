import sampleData from '../app/sampleData'
import React,{ useState, useEffect } from 'react'

function New({parentCallback}) {

    const [picked, setPicked] = useState([]);
    const [sites, setSites] = useState([]);
    const [list, setList] = useState([])

    const getSiteLists = async()=> {
        try{
           const response = (await fetch('http://127.0.0.1:3001/get-site-lists'));
           if (!response.ok){
            throw new Error(`HTTP error. Status: ${response.status}`)
           }
           const site_lists = await response.json();
           return site_lists
        }
        catch(error){
            console.error('getSiteLists failed');
            return null
        }
    }

    useEffect(()=>{
        const fetchSites = async()=> {
            const siteLists = await getSiteLists();
            if (siteLists){
                setSites(siteLists);
                console.log(`updating sites: ${siteLists}`)
            }
        }
        fetchSites();
    }, []);

    const handleSubmit = (e)=> {
        e.preventDefault();
        console.log(`picked: ${picked}`)
        parentCallback(picked);
    }

    const handleClick = (e)=> {
        e.preventDefault();
        const value = e.target.value;
        const tag = sites.find(item => item.tag === value);
        if (tag){    
            console.log(`updating list`)
            console.dir(tag)
            setList(tag)
        }
        else{
            console.log(`updating list`)
            console.dir(`list: ${tag}`)
            setList([]);
        }
    }

    const handleChange = (e)=> {
        setPicked((prevPicked)=> 
            e.target.checked ? [...prevPicked, e.target.value] : prevPicked.filter(i => i !== e.target.value)
        );
        console.log(e.target.value)
    };


    return(
        <div className='container'> 
        <form className="square">
            <p>Where would you like to go?</p>
            <div className='menu'>
                {sites.map((tag) =>
                    <button  type='button' className='button' id={tag.tag} value={tag.tag} onClick= { handleClick }>{ tag.tag }</button>
                    )}
            </div>
            {(list.list) && <div id='list'>
                {list.list.map((site) => 
                    <div key={site.id}>
                        <input type='checkbox' 
                               id={site.id} 
                               value={site.id}
                               onChange={ handleChange }>
                        </input>
                        <label htmlFor={site.id}>
                            {site.name}
                        </label>
                    </div>)
                    }
            </div>}
            <button className='button' onClick={handleSubmit}>Begin tour</button>
        </form>
        </div>
    )
}

export default New