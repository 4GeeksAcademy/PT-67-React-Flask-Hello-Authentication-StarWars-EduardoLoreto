import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/index.css";
import { FavoriteDropdown } from "./FavoriteDropdown";
import { Context } from "../store/appContext.js";  // Importa el Context

export const Navbar = () => {
    const { actions } = useContext(Context);  // Usa el Context para obtener las acciones
    const navigate = useNavigate();  // Para redirigir después del logout

    const handleLogout = async () => {
        await actions.logout();  // Llama a la acción logout
        navigate("/");  // Redirige a la página de login
    };

    return (
        <nav className="navbar bg-dark">
            <div>
                <img src="https://lumiere-a.akamaihd.net/v1/images/sw_logo_stacked_2x-52b4f6d33087_7ef430af.png?region=0,0,586,254"
                    className="logo ms-5" alt="logo-img" />
            </div>
            <div className="d-flex">
                <FavoriteDropdown />
                <button className="btn btn-danger ms-2" onClick={handleLogout}>
                    Logout
                </button>
            </div>
        </nav>
    );
};
