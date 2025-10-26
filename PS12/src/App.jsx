import { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";
import Login from "./registeration/Login";
import SignUp from "./registeration/SignUp";
import Home from "./registeration/home";
import Dashboard from "./registeration/dashboard";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "./firebase"; // import auth from top-level src/firebase.js

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // 👇 Track Firebase authentication state
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <Router>
      <Routes>
        {/* Public home landing page at root */}
        <Route path="/" element={<Home />} />

        {/* Auth routes - always accessible */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />

        {/* Protected home route (after authentication) */}
        <Route
          path="/home"
          element={user ? <Home /> : <Navigate to="/login" />}
        />
        {/* Protected dashboard route (after authentication) */}
        <Route
          path="/dashboard"
          element={user ? <Dashboard /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
