import React, { useState, useContext } from "react";
import { Context } from "../store/appContext.js";
import { useNavigate } from 'react-router-dom';
import "../../styles/home.css";

export const Login = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const logged = await actions.login(email, password);
            if (logged) {
                navigate("/home");
            } else {
                setError("Credenciales inválidas. Por favor, intente nuevamente.");
            }
        } catch (err) {
            setError("Ocurrió un error al iniciar sesión. Inténtelo nuevamente más tarde.");
        }
    };

    return (
        <div className="container-fluid justify-content-center text-white w-25">
            <form className="form-login mt-5" onSubmit={handleLogin}>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email address</label>
                    <input value={email} onChange={(e) => setEmail(e.target.value)}
                        type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input value={password} onChange={(e) => setPassword(e.target.value)}
                        type="password" className="form-control" id="password1" aria-describedby="password" placeholder="Enter Password" />
                </div>
                <div className="container-fluid d-flex justify-content-center w-25">
                    <button type="submit" className="btn btn-warning btn-lg w-100">Login</button>
                </div>
                {error && <p>{error}</p>}
            </form>
        </div>
    );
};
