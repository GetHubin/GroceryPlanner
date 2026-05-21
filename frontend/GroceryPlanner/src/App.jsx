import { useState } from 'react'
import './App.css'

function App() {
    const [searchBar, setText] = useState("");
    const [searchList, setSearchList] = useState([]);
    const [cartList, setCartList] = useState([]);

    function searching() {
        fetch(`http://localhost:8080/search/${searchBar}`)
            .then(res => res.json())
            .then(data => {setSearchList(data)})
    }
    function productBox(item){
        <div className={"itemBox"}>
            <h2>{item.name}</h2>
            <p>${item.price}</p>
        </div>
    }

    return(
      <div className={"main-container"}>
        <div className={"searchPanel"}>search</div>
            <input type={"text"}
                   value={searchBar}
                   placeholder="Type here..." onChange={(e) => setText(e.target.value)}>
            </input>
            <button onClick={() => searching()}>Submit</button>
            {searchList.map((item, index) =>
                <p key={index}>{item}</p>
            ))}
            <div className={"searchItemList"}></div>
        <div className={"cartPanel"}>cart</div>
      </div>
    )
}

export default App
