import {useEffect, useState} from 'react'
import '../css/Grocery.css'

function App() {
    const [searchBar, setText] = useState("");
    const [searchList, setSearchList] = useState([]);
    const [cartList, setCartList] = useState([]);
    const [selectedInfo, setSelectedInfo] = useState("");
    const totalPrice = cartList.reduce((sum, item) => {
        return sum + ((item?.price ?? 0) * item.quantity);
    }, 0);

    function decrement(item) {
        if (item.quantity > 0) {
            setCartList(prev =>
                prev.map(cartItem =>
                    cartItem.productId === item.productId
                        ? {
                            ...cartItem,
                            quantity: cartItem.quantity - 1
                        }
                        : cartItem
                )
            );
            setSearchList(prev =>
                prev.map(searchItem =>
                    searchItem.productId === item.productId
                        ? {
                            ...searchItem,
                            quantity: searchItem.quantity - 1
                        }
                        : searchItem
                )
            );
        }
    }
    function increment(item) {
        setCartList(prev =>
            prev.map(cartItem =>
                cartItem.productId === item.productId
                    ? {
                        ...cartItem,
                        quantity: cartItem.quantity + 1
                    }
                    : cartItem
            )
        );
        setSearchList(prev =>
            prev.map(searchItem =>
                searchItem.productId === item.productId
                    ? {
                        ...searchItem,
                        quantity: searchItem.quantity + 1
                    }
                    : searchItem
            )
        );
    }


    function searching() {
        fetch(`http://localhost:8000/search/${searchBar}/${localStorage.getItem("currUser")}`)
            .then(res => res.json())
            .then(res => {setSearchList(res)})
    }


    function productBox(item) {
        console.log(item);
        return (
            <div className="itemBox">
                <h2>{item.description}</h2>

                <p>
                    ${item.price ?? NaN}
                </p>

                <button onClick={() => decrement(item)}>-1</button>

                <p>{item.quantity ?? 1}</p>

                <button onClick={() => increment(item)}>+1</button>

                {!cartList.some(
                    cartItem => cartItem.productId === item.productId
                ) && (
                    <button onClick={() =>
                        setCartList(prev => [...prev, item])
                    }>
                        add to cart
                    </button>
                )}

                {cartList.some(
                    cartItem => cartItem.productId === item.productId
                ) && (
                    <button onClick={() =>
                        setCartList(prev =>
                            prev.filter(
                                cartItem => cartItem.productId !== item.productId
                            )
                        )
                    }>
                        remove from cart
                    </button>
                )}
                <button onClick={() => setSelectedInfo(item.description)}>i</button>
                {selectedInfo === item.description && (
                    <div className={"infoBox"}>{informationBox(item)}</div>)}
            </div>
        );
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
    function saveCart(){
        const items= cartList.map(product => ({"itemId": product.productId, "quantity": product.quantity}));
        fetch(`http://localhost:8000/accounts/${localStorage.getItem("currUser")}/cart`,
            {"method": "PATCH", body: JSON.stringify({"items" : items}),
                "headers": {"Content-Type": "application/json"}})
    }

    function prevCart(){
        fetch(`http://localhost:8000/accounts/${localStorage.getItem("currUser")}/savedCart`,
            {"method": "GET", "headers": {"Content-Type": "application/json"}})
            .then(res => res.json())
            .then(res =>
            {if(res.message !== "User not found"){
                if(res.length === 0){
                    setCartList([])
                }
                Promise.all(
                    res.map(item =>
                        fetch(
                            `http://localhost:8000/products/${item.item_id}/${localStorage.getItem("currUser")}`
                        )
                            .then(r => r.json())
                            .then(product => ({
                                ...product,
                                quantity: item.quantity
                            }))
                    )
                ).then(products => {
                    setCartList(products);
                });
            }
            })
    }
    useEffect(() => {
        prevCart()
    }, []);

    return(
        <div className={"main-container"}>
            <div className={"searchPanel"}>search
                <input type={"text"}
                       value={searchBar}
                       placeholder="Type here..." onChange={(e) => setText(e.target.value)}>
                </input>
                <button onClick={() => searching()}>Submit</button>
                {searchList.map((item, index) =>
                    <div key={index}>{productBox(item)}</div>
                )}
            </div>
            <div className={"cartPanel"}>cart
                <div className="cartItems">
                    {cartList.map((item, index) =>
                        <div key={index}>{productBox(item)}</div>
                    )}
                </div>
                <div className={"totalBox"}>total: {totalPrice}
                    <button onClick={() => setCartList([])}>empty cart</button>
                    <button onClick={() => saveCart()}>save cart</button>
                </div>
            </div>
        </div>
    )
}

export default App
