import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../store/slices/authSlice';

const Layout = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useSelector(state => state.auth);
  
  const handleLogout = () => {
    dispatch(logout());
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    navigate('/login');
  };
  
  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">🛒 E-commerce</Link>
        </div>
        <div className="nav-links">
          <Link to="/products">Products</Link>
          {isAuthenticated && (
            <>
              <Link to="/orders">Orders</Link>
              <Link to="/profile">{user?.email}</Link>
              <button onClick={handleLogout} className="btn-logout">Logout</button>
            </>
          )}
          {!isAuthenticated && (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </nav>
      
      <main className="main-content">
        <Outlet />
      </main>
      
      <footer className="footer">
        <p>&copy; 2026 Enterprise DevSecOps E-commerce Platform. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
