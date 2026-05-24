import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { userService } from '../services/authService';

const Profile = () => {
  const user = useSelector(state => state.auth.user);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: ''
  });
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: ''
  });
  
  useEffect(() => {
    loadProfile();
  }, []);
  
  const loadProfile = async () => {
    try {
      setLoading(true);
      const response = await userService.getProfile();
      setProfile(response.data);
      setFormData({
        first_name: response.data.first_name,
        last_name: response.data.last_name
      });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };
  
  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      await userService.updateProfile(formData);
      loadProfile();
      setEditMode(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update profile');
    }
  };
  
  const handleChangePassword = async (e) => {
    e.preventDefault();
    try {
      await userService.changePassword(
        passwordForm.current_password,
        passwordForm.new_password
      );
      setPasswordForm({ current_password: '', new_password: '' });
      setError('');
      alert('Password changed successfully');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to change password');
    }
  };
  
  if (loading) return <div className="loading">Loading profile...</div>;
  
  return (
    <div className="profile-container">
      <h1>User Profile</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      {profile && (
        <>
          <div className="profile-section">
            <h2>Personal Information</h2>
            {editMode ? (
              <form onSubmit={handleUpdateProfile}>
                <div className="form-group">
                  <label>First Name:</label>
                  <input
                    type="text"
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Last Name:</label>
                  <input
                    type="text"
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                  />
                </div>
                <button type="submit" className="btn-primary">Save</button>
                <button type="button" className="btn-secondary" onClick={() => setEditMode(false)}>Cancel</button>
              </form>
            ) : (
              <div>
                <p><strong>Email:</strong> {profile.email}</p>
                <p><strong>First Name:</strong> {profile.first_name}</p>
                <p><strong>Last Name:</strong> {profile.last_name}</p>
                <p><strong>Roles:</strong> {profile.roles.join(', ')}</p>
                <button className="btn-primary" onClick={() => setEditMode(true)}>Edit</button>
              </div>
            )}
          </div>
          
          <div className="profile-section">
            <h2>Change Password</h2>
            <form onSubmit={handleChangePassword}>
              <div className="form-group">
                <label>Current Password:</label>
                <input
                  type="password"
                  value={passwordForm.current_password}
                  onChange={(e) => setPasswordForm({...passwordForm, current_password: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>New Password:</label>
                <input
                  type="password"
                  value={passwordForm.new_password}
                  onChange={(e) => setPasswordForm({...passwordForm, new_password: e.target.value})}
                  required
                />
                <small>Min 12 chars, uppercase, lowercase, digit, special char</small>
              </div>
              <button type="submit" className="btn-primary">Change Password</button>
            </form>
          </div>
        </>
      )}
    </div>
  );
};

export default Profile;
