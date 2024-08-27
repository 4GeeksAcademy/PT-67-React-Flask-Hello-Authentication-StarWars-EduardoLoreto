import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Signup = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const validatePassword = (password) => {
        // Ejemplo básico: la contraseña debe tener al menos 8 caracteres
        return password.length >= 8;
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");

        if (!validateEmail(email)) {
            setError("El email no es válido");
            return;
        }

        if (!validatePassword(password)) {
            setError("La contraseña debe tener al menos 8 caracteres");
            return;
        }

        try {
            const response = await fetch("https://refactored-space-xylophone-9799xjp76g47hw6r-3001.app.github.dev/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                throw new Error(errorMessage);
            }

            const data = await response.json();
            navigate("/login"); // Redirigir al login después de un registro exitoso
        } catch (error) {
            setError(error.message || "Error al registrarse. Por favor, intente nuevamente.");
        }
    };

    return (
        <div>
            <h2>Signup</h2>
            {error && <p>{error}</p>}
            <form onSubmit={handleSignup}>
                <div>
                    <label>Email:</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
};
