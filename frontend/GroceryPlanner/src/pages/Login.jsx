import { useNavigate } from "react-router-dom";
import '../css/Login.css'
import {useState} from "react";

function Login() {
    const [Username, setUsername] = useState("");
    const [Password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
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
            else{
                setErrorMessage("username or password is incorrect or user does not exist.");
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
            else{
                setErrorMessage("username already exist.");
            }
        })
}

    return (
        <div className="login-page">
            <div className="login-box">
                <h1>Welcome</h1>
                <p>Sign in or create an account.</p>

                <input
                    type="text"
                    value={Username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />

                <input
                    type="password"
                    value={Password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <p>{errorMessage}</p>
                <button onClick={login}>Login</button>
                <button onClick={signup}>Sign Up</button>

            </div>
        </div>
    );
}

export default Login;