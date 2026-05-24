import React, { useEffect, useState } from 'react';
import { orderService } from '../services/authService';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    loadOrders();
  }, []);
  
  const loadOrders = async () => {
    try {
      setLoading(true);
      const response = await orderService.getOrders();
      setOrders(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load orders');
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancelOrder = async (orderId) => {
    try {
      await orderService.cancelOrder(orderId);
      loadOrders();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to cancel order');
    }
  };
  
  return (
    <div className="orders-container">
      <h1>My Orders</h1>
      
      {error && <div className="error-message">{error}</div>}
      {loading && <div className="loading">Loading orders...</div>}
      
      {orders.length === 0 ? (
        <p>No orders yet.</p>
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <h3>Order #{order.id}</h3>
                <span className={`status ${order.status}`}>{order.status}</span>
              </div>
              
              <p><strong>Total:</strong> ${order.total.toFixed(2)}</p>
              <p><strong>Items:</strong> {order.items.length}</p>
              <p><strong>Created:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
              
              <div className="order-items">
                {order.items.map((item, idx) => (
                  <div key={idx} className="item">
                    Product #{item.product_id} x {item.quantity}
                  </div>
                ))}
              </div>
              
              {(order.status === 'pending' || order.status === 'confirmed') && (
                <button 
                  className="btn-danger"
                  onClick={() => handleCancelOrder(order.id)}
                >
                  Cancel Order
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;
