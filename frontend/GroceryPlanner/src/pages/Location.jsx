import { useNavigate } from "react-router-dom";
import '../css/Location.css'
import {useState} from "react";

function Location() {
    const [zip, setZip] = useState("")
    const navigate = useNavigate();
    const [locationList, setLocationList] = useState([]);

    function findLocations(zip) {
        setZip(zip);
        fetch(`http://localhost:8000/locations/${zip}`,
            {"method": "GET", headers: {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(locationList => setLocationList(locationList))
    }
    function modifyLocation(location) {
        fetch(`http://localhost:8000/locations/${location.locationId}`, {method: "PATCH", headers: {"Content-Type": "application/json"}} )
    }
    function locationBox(location){
        console.log(location)
        return <div className="location-box">
            <h3>{location.name} </h3>
            <p>id: {location.storeNumber} at {location.address}</p>
            <button onClick={() => {
                modifyLocation(location);
                navigate("/grocery")
            }}>this location</button>
        </div>
    }
    return (
        <div className="locationPanel">
            <h1>Store Locator</h1>
            <div className={"locationInput"}>
                <p>input zip code</p>
                <input type={"text"}
                             value={zip}
                             placeholder="Type here..." onChange={(e) => setZip(e.target.value)}>
                </input>
                <button onClick={() => findLocations(zip)}>Submit</button>
                <h1>OR</h1>
                <button>use current Location</button>
            </div>
            <div className={"locationsContainer"}>
            {locationList.map((location, index) =>
                <div key={index}>{locationBox(location)}</div>)
            }
            </div>
            <button onClick={() => navigate("/grocery")}>
                Start Shopping
            </button>
        </div>
    )
}

export default Location;