import { useNavigate } from "react-router-dom";

function Location() {

    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome</h1>

            <button onClick={() => navigate("/grocery")}>
                Start Shopping
            </button>
        </div>
    )
}

export default Location;