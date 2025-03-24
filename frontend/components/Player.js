export default function Player({url}){
    const src = url.startsWith('http') ? url : `https://${url}`;
    return(
        <div className='player'>
            <iframe 
                src={src}
                allow='autoplay'
                allowFullScreen
            ></iframe>
        </div>
    )
}