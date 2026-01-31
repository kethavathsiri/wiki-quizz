import axios from 'axios';
import { useState } from 'react';
import './Auth.css';

function Register({ apiBaseUrl, onLogin, onError }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    onError('');
    try {
      const resp = await axios.post(`${apiBaseUrl}/api/auth/register`, { email, password, full_name: fullName });
      // After registration, auto-login
      const loginResp = await axios.post(`${apiBaseUrl}/api/auth/login`, { email, password });
      const token = loginResp.data.access_token;
      localStorage.setItem('token', token);
      onLogin(token);
    } catch (err) {
      console.error(err);
      onError('Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form">
      <h3>Register</h3>
      <form onSubmit={handleSubmit}>
        <input placeholder="Full name (optional)" value={fullName} onChange={e => setFullName(e.target.value)} />
        <input placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button className="btn-primary" type="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
      </form>
    </div>
  );
}

export default Register;
