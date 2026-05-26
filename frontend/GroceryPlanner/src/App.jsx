import {
    Routes,
    Route
} from "react-router-dom";

import Login from "./pages/Login.jsx";
import Grocery from "./pages/Grocery.jsx";
import Location from "./pages/Location.jsx";

function App() {

    return (
        <Routes>

            <Route
                path="/"
                element={<Login />}
            />

            <Route
                path="/Location"
                element={<Location />}
            />

            <Route
                path="/grocery"
                element={<Grocery />}
            />

        </Routes>
    )
}

export default App;