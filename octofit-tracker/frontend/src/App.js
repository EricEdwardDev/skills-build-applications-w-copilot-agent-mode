import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import './App.css';
import { AuthProvider, useAuth } from './AuthContext';
import { logout as apiLogout } from './api';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';

function AppContent() {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = async () => {
    await apiLogout();
    logout();
    navigate('/login');
  };

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            <img 
              src="/octofitapp-logo.png" 
              alt="OctoFit Logo" 
              className="navbar-logo"
            />
            OctoFit Tracker
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              {isAuthenticated && (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/activities">
                      Activities
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/leaderboard">
                      Leaderboard
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/teams">
                      Teams
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/users">
                      Users
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/workouts">
                      Workouts
                    </Link>
                  </li>
                  <li className="nav-item">
                    <span className="nav-link">
                      Welcome, {user?.username || 'User'}!
                    </span>
                  </li>
                  <li className="nav-item">
                    <button 
                      className="btn btn-outline-light btn-sm" 
                      onClick={handleLogout}
                    >
                      Logout
                    </button>
                  </li>
                </>
              )}
              {!isAuthenticated && (
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    Login
                  </Link>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>

      <main className="py-5">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <div className="container">
                <div className="jumbotron">
                  <h1 className="display-4">Welcome to OctoFit Tracker</h1>
                  <p className="lead">
                    Track your fitness activities, compete on leaderboards, and achieve your goals!
                  </p>
                  {!isAuthenticated && (
                    <p className="mt-3">
                      <Link className="btn btn-primary btn-lg" to="/login">
                        Login to Get Started
                      </Link>
                    </p>
                  )}
                  {isAuthenticated && (
                    <p className="mt-3">Use the navigation menu above to explore different features.</p>
                  )}
                </div>
              </div>
            }
          />
          <Route 
            path="/activities" 
            element={
              <ProtectedRoute>
                <Activities />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/leaderboard" 
            element={
              <ProtectedRoute>
                <Leaderboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/teams" 
            element={
              <ProtectedRoute>
                <Teams />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/users" 
            element={
              <ProtectedRoute>
                <Users />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/workouts" 
            element={
              <ProtectedRoute>
                <Workouts />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </main>

      <footer className="bg-dark text-white text-center py-4 mt-5">
        <p>&copy; 2024 OctoFit Tracker. All rights reserved.</p>
      </footer>
    </div>
  );
}

function App() {
  console.log('App component loaded');
  console.log('React App Codespace Name:', process.env.REACT_APP_CODESPACE_NAME || 'localhost');

  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
