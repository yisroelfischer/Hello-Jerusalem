import React, { useState, useEffect } from "react";
import Chat from "./Chat";
import Error from "./Error";

function New({ parentCallback }) {
  console.log("hello");
  const [picked, setPicked] = useState([]);
  const [sites, setSites] = useState([]);
  const [list, setList] = useState([]);

  // Lists of sites organized by tag
  const getSiteLists = async () => {
    console.log("getSiteLists");
    try {
      const response = await fetch("http://localhost:5000/get-site-lists");
      if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`);
      }
      const site_lists = await response.json();
      return site_lists;
    } catch (error) {
      console.error("getSiteLists failed");
      return null;
    }
  };

  useEffect(() => {
    console.log("useEffect");
    const fetchSites = async () => {
      const siteLists = await getSiteLists();
      if (siteLists) {
        setSites(siteLists);
        setList(siteLists[0]);
      }
    };
    fetchSites();
  }, []);

  const handleSubmit = (e) => {
    console.log("handleSubmit");
    e.preventDefault();
    console.log(`picked: ${picked}`);
    parentCallback(picked);
  };

  const handleClick = (e) => {
    const value = e.target.value;
    const tag = sites.find((item) => item.tag === value);
    if (tag) {
      setList(tag);
    } else {
      return (
        <>
          <Error />
        </>
      );
    }
  };

  useEffect(() => {
    // Style tab
    const tabs = document.getElementsByClassName("tab");
    for (let i = 0; i < tabs.length; i++) {
      const tab = tabs[i];
      console.log(tab);
      if (tab.id === list.tag) {
        tab.style.backgroundColor = "var(--background)";
        tab.style.borderTop = '1px solid var(--accent)';
        tab.style.borderBottom = '1px solid var(--accent)';
      } else {
        tab.style.backgroundColor = "transparent";
        tab.style.borderTop = 'none';
        tab.style.borderBottom = 'none';
      }
    }
  }, [list]);

  const handleChange = (e) => {
    console.log("handleChange");
    setPicked((prevPicked) =>
      e.target.checked
        ? [...prevPicked, e.target.value]
        : prevPicked.filter((i) => i !== e.target.value)
    );
    console.log(e.target.value);
  };

  return (
    <div className="container">
      <Chat
        context={`The user is on a page where they can select from a list of sites they want
            to visit. When they click the Begin Tour button, the site will automatically calculate
            a tour visiting those sites from the videos in its database. The sites are arranged by
            tags. The user can see the list of sites for each tag by clicking or tapping its tab`}
      />
      <form>
        <div className="form-head">
          <h2>Select the sites you want to visit</h2>
        </div>
        <div className="form-main">
          <div className="tabs" id="tabs">
            {sites.map((tag) => (
              <button
                type="button"
                key={tag.tag}
                className="tab"
                id={tag.tag}
                value={tag.tag}
                onClick={handleClick}
              >
                {tag.tag}
              </button>
            ))}
          </div>
          {list.list && (
            <div id="list" className="list">
              {list.list.map((site) => (
                <div className="check-border" key={site.id}>
                  <div key={site.id} className="check-container">
                    <input
                      type="checkbox"
                      className="check"
                      id={site.id}
                      value={site.id}
                      onChange={handleChange}
                    ></input>
                    <label htmlFor={site.id} className="check-label">
                      {site.name}
                    </label>
                  </div>
                </div>
              ))}
            </div>
          )}
          <button className="button" onClick={handleSubmit}>
            Begin
          </button>
        </div>
       
      </form>
    </div>
  );
}

export default New;
