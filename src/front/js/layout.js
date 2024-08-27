import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/ScrollToTop";
import { Home } from "./views/Home";
import { ItemDetails } from "./views/ItemDetails";
import { Signup } from "./component/Signup";
import { Login } from "./component/Login";
import { PrivateRoute } from "./component/PrivateRoute";
import { Navbar } from "./component/Navbar";
import { Footer } from "./component/Footer";
import injectContext from "./store/appContext";

function Layout() {
    const basename = process.env.BASENAME || "";
    

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route path="/" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route
                            path="/home"
                            element={<PrivateRoute>
                                <Home />
                            </PrivateRoute>} />
                        <Route path="learn/:type/:uid" element={<ItemDetails />} />
                        <Route path="*" element={<h1>Not found!</h1>} />
                    </Routes>
                    <Footer />
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
}

export default injectContext(Layout);
