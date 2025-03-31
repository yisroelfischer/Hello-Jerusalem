export default function TourMenu({
  links,
  isLastTour,
  isLastSite,
  handleClick,
  children,
}) {
  return (
    <div className="tour-menu">
      {links && (
        <div className="links">
          {links.map((link) => {
            <a href={link.link} id={link.id}>
              {link.name}
            </a>;
          })}
        </div>
      )}
      <button className="next-button button" onClick={handleClick}>
        {!isLastSite && "Continue"}
        {isLastSite && !isLastTour && "Next Tour"}
        {isLastSite && isLastTour && "Back to Home"}
      </button>
    </div>
  );
}
