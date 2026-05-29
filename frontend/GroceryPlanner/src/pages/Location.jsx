import { useNavigate } from "react-router-dom";
import '../css/Location.css'
import {useEffect, useState} from "react";

function Location() {
    const [zip, setZip] = useState("")
    const navigate = useNavigate();
    const [locationList, setLocationList] = useState([]);

    function updateUserLocations(location){
        fetch(`http://localhost:8000/accounts/${localStorage.getItem("currUser")}/locations`,
            {"method": "PATCH", body: JSON.stringify({"locationId" : location.locationId}),
                "headers": {"Content-Type": "application/json"}})
    }

    function findWId(locationId){
        fetch(`http://localhost:8000/locations/${locationId}/id`,
            {"method": "GET", headers: {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(locationList => setLocationList(locationList))
    }
    function findWZip(zip) {
        setZip(zip);
        fetch(`http://localhost:8000/locations/${zip}/zip`,
            {"method": "GET", headers: {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(locationList => setLocationList(locationList))
    }
    function findWLocation(){
        navigator.geolocation.getCurrentPosition(
            (position) => {
                console.log(position.coords.latitude);
                console.log(position.coords.longitude);
                fetch(`http://localhost:8000/locations/${position.coords.latitude}/${position.coords.longitude}`,
                    {method: "GET", headers: {"Content-Type": "application/json"}})
                    .then(res => res.json())
                    .then(locationList => setLocationList(locationList))
            }
        )
    }
    function modifyLocation(location) {
        fetch(`http://localhost:8000/accounts/${localStorage.getItem("currUser")}/locations`,
            {method: "PATCH", headers: {"Content-Type": "application/json"}, "body": JSON.stringify({"locationId": location.locationId})} )
    }
    function locationBox(location){
        console.log(location)
        return <div className="location-box">
            <h3>{location.name} </h3>
            <p>id: {location.storeNumber} at {location.address}</p>
            <button onClick={() => {
                modifyLocation(location);
                updateUserLocations(location);
                navigate("/grocery")
            }}>this location</button>
        </div>
    }

    function prevLocations(){
        fetch(`http://localhost:8000/accounts/${localStorage.getItem("currUser")}/prevLocations`,
            {"method": "GET", "headers": {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(res =>
            {if(res.message !== "User not found"){
                for(let i=0; i<res.length; i++ ){
                    findWId(res[i]);
                }
            }
            })
    }
    useEffect(() => {
        prevLocations()
    }, []);

    return (
        <div className="locationPanel">
            <h1>Store Locator</h1>
            <div className={"locationInput"}>
                <p>input zip code</p>
                <input type={"text"}
                             value={zip}
                             placeholder="Type here..." onChange={(e) => setZip(e.target.value)}>
                </input>
                <button onClick={() => findWZip(zip)}>Submit</button>
                <h1>OR</h1>
                <button onClick={findWLocation}>use current Location</button>
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