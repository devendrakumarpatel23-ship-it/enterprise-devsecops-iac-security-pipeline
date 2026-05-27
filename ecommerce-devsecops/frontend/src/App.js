import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Products from './pages/Products';
import OrdersPage from './pages/Orders';
import Profile from './pages/Profile';
import SOCDashboard from './pages/SOCDashboard';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/products" replace />} />
            <Route path="/products" element={<Products />} />
            <Route path="/soc" element={<SOCDashboard />} />
            
            <Route element={<PrivateRoute />}>
              <Route path="/orders" element={<OrdersPage />} />
              <Route path="/profile" element={<Profile />} />
            </Route>
          </Route>
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
