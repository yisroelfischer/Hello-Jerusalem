export default function Error({error=0}){
    return(
        <>
        <div className="errorCode">{ error }</div>
        <div className="message">Something went wrong</div>
        </>
    )
}