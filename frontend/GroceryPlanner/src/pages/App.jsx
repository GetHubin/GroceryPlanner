import {
    Routes,
    Route
} from "react-router-dom";

import Home from "./pages/Home";
import Grocery from "./Grocery.jsx";
import Location from "./pages/Loctation";

function App() {

    return (
        <Routes>

            <Route
                path="/"
                element={<Home />}
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