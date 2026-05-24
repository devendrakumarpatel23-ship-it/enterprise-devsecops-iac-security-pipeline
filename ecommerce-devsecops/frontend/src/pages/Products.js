import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { productService } from '../services/authService';
import { fetchStart, fetchSuccess, fetchFailure } from '../store/slices/productSlice';

const Products = () => {
  const dispatch = useDispatch();
  const { products, loading, error, pagination } = useSelector(state => state.products);
  const [page, setPage] = useState(1);
  const [category, setCategory] = useState('');
  
  useEffect(() => {
    loadProducts();
  }, [page, category]);
  
  const loadProducts = async () => {
    dispatch(fetchStart());
    try {
      const response = await productService.getProducts(page, 10, category);
      dispatch(fetchSuccess(response));
    } catch (err) {
      dispatch(fetchFailure(err.message));
    }
  };
  
  return (
    <div className="products-container">
      <h1>Products</h1>
      
      <div className="filters">
        <input
          type="text"
          placeholder="Filter by category"
          value={category}
          onChange={(e) => {
            setCategory(e.target.value);
            setPage(1);
          }}
        />
      </div>
      
      {error && <div className="error-message">{error}</div>}
      {loading && <div className="loading">Loading products...</div>}
      
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p className="price">${product.price.toFixed(2)}</p>
            <p className="stock">Stock: {product.stock}</p>
            <p className="rating">⭐ {product.rating}</p>
            <button className="btn-primary">Add to Cart</button>
          </div>
        ))}
      </div>
      
      <div className="pagination">
        <button 
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >Previous</button>
        <span>Page {pagination.page} of {pagination.pages}</span>
        <button
          disabled={page === pagination.pages}
          onClick={() => setPage(page + 1)}
        >Next</button>
      </div>
    </div>
  );
};

export default Products;
