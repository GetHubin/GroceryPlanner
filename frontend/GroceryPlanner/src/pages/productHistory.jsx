import {useEffect, useState} from 'react'
import '../css/productHistory.css'
import {useNavigate} from "react-router-dom";

function App(){
    const navigate = useNavigate();
    const [pickedProduct, setPickedProduct] = useState(null);
    const [selectedInfo, setSelectedInfo] = useState("");
    const [historyList, setHistoryList] = useState([]);
    const [historyData, setHistoryData] = useState([]);

    //info["product_id"], info["user_id"], info["regular_price"], info["promo_price"]
    function addItemToPriceHistory(item){
        const data = {
            product_id: item.productId,
            user_id: localStorage.getItem("currUser"),
            regular_price: item.price,
            promo_price: item.promoPrice,
        }
        fetch(`http://localhost:8000/priceHistory/addProduct`,
            {method: "POST", body: JSON.stringify(data), headers: {"Content-Type": "application/json"}})
    }

    function removeItemFromPriceHistory(){
        fetch(`http://localhost:8000/priceHistory/${pickedProduct.productId}`, {method: "DELETE", headers: {"Content-Type": "application/json"}})
    }

    function getPriceHistory(item){
        fetch(`http://localhost:8000/priceHistory/${item.productId}`, {method: "GET", headers: {"Content-Type": "application/json"}})
            .then (res => res.json())
            .then(data => {setHistoryData(data); console.log(data)})
    }

    function informationBox(item) {
        return(
            <div className="infoPanel">
                <h1>{item.description}</h1>
                <img
                    src={item.imageUrl || "/placeholder.png"}
                    alt={item.description}
                    style={{ width: "150px", height: "150px" }}
                />
                <button onClick={() => setSelectedInfo("")}>close</button>
                <p>{item.aisleLocations}</p>
                <p>{item.manufacturerDeclarations}</p>
                <p>{item.allergensDescription}</p>
                <p>${item.price}</p>
            </div>
        )
    }

    function productBox(item) {
        return (
            <div className="itemBox">
                <h2>{item.description}</h2>
                {(pickedProduct?.productId !== item.productId
                ) && (
                    <button onClick={() => {
                        setPickedProduct(item);
                        getPriceHistory(item);
                    }}>
                        select
                    </button>
                )}

                {(pickedProduct?.productId === item.productId
                ) && (
                    <button onClick={() =>
                        setPickedProduct(null)
                    }>
                        deselect
                    </button>
                )}
                <button onClick={() => setSelectedInfo(item.productId)}>i</button>
                {selectedInfo === item.productId && (
                    <div className={"infoBox"}>{informationBox(item)}</div>
                )}
            </div>
        );
    }

    function getPriceHistoryList(){
        //fetch the item_id's and then search by id to get the item info then
        fetch(`http://localhost:8000/priceHistory/getPriceHistoryList/${localStorage.getItem("currUser")}`,
            {"method": "GET", headers: {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(data => {setHistoryList(data)})
            .then(data => console.log(data))
    }

    useEffect(() => {
        getPriceHistoryList()
    }, []);

    return (
        <div className="main-container">
            <div className={"sidePanel"}>products
                {historyList.map((item, index) =>
                    <div key={index}>{productBox(item)}</div>
                )}
                <div className={"buttons"}>
                    <button onClick={removeItemFromPriceHistory}>remove history</button>
                    {<button onClick={() => navigate("/Grocery")}>
                        back to Shopping
                    </button>}
                </div>
            </div>
            <div className={"historyPanel"}>info
                {pickedProduct && <h1>{pickedProduct.description}</h1>}
                {historyData.map((entry, index) => (
                    <p key={index}>
                        ${entry.week_date}
                        ${entry.promo_price}
                        ${entry.norm_price}
                    </p>
                ))}
            </div>
        </div>
    )
}

export default App