export default function Player({url}){
    return(
        <div className='player'>
            <iframe 
                src={url}
                allow='autoplay'
                allowFullScreen
            ></iframe>
        </div>
    )
}