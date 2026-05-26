import { useNavigate } from "react-router-dom";
import '../css/Login.css'

function Login() {

    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome</h1>

            <button onClick={() => navigate("/location")}>
                Start Shopping
            </button>
        </div>
    )
}

export default Login;