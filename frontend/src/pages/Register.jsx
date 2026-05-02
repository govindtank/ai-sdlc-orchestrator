import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Box, TextField, Button, Typography, Container, Paper, Alert, Link as MuiLink } from '@mui/material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await axios.post(`${API_BASE_URL}/auth/register`, formData);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  if (success) return <Navigate to="/login" replace />;

  return (
    <Container maxWidth="sm">
      <Paper sx={{ p: 4, mt: 8 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h4" gutterBottom component="div">
            Create Account
          </Typography>
          <Typography color="text.secondary">Join AI SDLC Orchestrator</Typography>
        </Box>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
        )}
        
        <form onSubmit={handleRegister}>
          <TextField
            fullWidth
            label="Full Name"
            name="full_name"
            margin="normal"
            value={formData.full_name}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            margin="normal"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            margin="normal"
            value={formData.password}
            onChange={handleChange}
            required
            helperText="Minimum 6 characters"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </Button>
        </form>
        
        <Typography sx={{ textAlign: 'center', mt: 2, pt: 2 }}>
          Already have an account? <a href="/login" style={{ color: 'primary.main' }}>Login</a>
        </Typography>
      </Paper>
    </Container>
  );
}

export default Register;
