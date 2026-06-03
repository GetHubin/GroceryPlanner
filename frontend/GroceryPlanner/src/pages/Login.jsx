import { useNavigate } from "react-router-dom";
import '../css/Login.css'
import {useState} from "react";

function Login() {
    const [Username, setUsername] = useState("");
    const [Password, setPassword] = useState("");
    const navigate = useNavigate();

function login()
{
    fetch("http://localhost:8000/accounts/login", {
        method: "POST",
        body: JSON.stringify({username: Username, password: Password}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === "success"){
                localStorage.setItem("currUser", data.userId);
                navigate("/Location");
            }
        })
}
function signup(){
    fetch("http://localhost:8000/accounts/signup", {
        method: "POST",
        body: JSON.stringify({username: Username, password: Password}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === "success"){
                localStorage.setItem("currUser", data.userId);
                navigate("/Location");
            }
        })
}

    return (
        <div>
            <h1>Welcome please sign in or sign up here</h1>
            <input type="text"
                onChange={(e) => setUsername(e.target.value)}
                value={Username}
                placeholder="type Username here"/>
            <input type="text"
                onChange={(e) => setPassword(e.target.value)}
                value={Password}
                placeholder="type Password here"/>
            <button onClick={() => login()}>login</button>
            <button onClick={() => signup()}>signup</button>
            {<button onClick={() => navigate("/location")}>
                Start Shopping
            </button>}
        </div>
    )
}

export default Login;