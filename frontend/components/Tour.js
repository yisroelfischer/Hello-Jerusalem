import React, {useState} from 'react'
import Player from './Player'

export default function Tour({tour}) {
    const [current, setCurrent] = useState(0)
    const [video, setVideo] = useState('https://www.youtube.com/embed/728II869JfM?start=1100&chromeless=true')

    const getVideo = async() => {
        try{
            const url = `http://127.0.0.1:3001/get-video?path=${tour[current]}`
            const response = await fetch(url);
            if (!response.ok){
                throw new Error(`HTTP error. Status: ${response.status}`)
            }
            const result = await response.json()
            setVideo(result)
            setCurrent((prev)=> prev + 1)
        } catch (error) {
            console.error('getTour failed');
            return null
        }
        
    }

    return(
        <Player url={video}/>
    )
}