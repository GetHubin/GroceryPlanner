import { useNavigate } from "react-router-dom";

function Login() {

    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome</h1>

            <button onClick={() => navigate("/loctation")}>
                Start Shopping
            </button>
        </div>
    )
}

export default Login;