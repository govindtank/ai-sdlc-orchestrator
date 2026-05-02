import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, Typography, TextField, Button, Chip, Container, Grid, Alert
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Requirements() {
  const navigate = useNavigate();
  const [requirements, setRequirements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    raw_text: '',
  });

  useEffect(() => {
    fetchRequirements();
  }, []);

  const fetchRequirements = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/requirements`);
      setRequirements(res.data);
    } catch (err) {
      console.error('Failed to load requirements:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await axios.post(`${API_BASE_URL}/requirements`, formData);
      fetchRequirements();
      setFormData({ raw_text: '' });
      setShowForm(false);
      alert('Requirement created successfully!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create requirement');
    }
  };

  if (loading) return <Typography>Loading requirements...</Typography>;

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Requirements</Typography>
          <Button variant="contained" onClick={() => setShowForm(true)}>
            + Add New Requirement
          </Button>
        </Box>
      </Paper>

      {showForm && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Add New Requirement</Typography>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Requirement Text"
            value={formData.raw_text}
            onChange={(e) => setFormData({ ...formData, raw_text: e.target.value })}
            sx={{ mb: 2 }}
          />
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="contained" onClick={handleCreate}>Create</Button>
            <Button variant="outlined" onClick={() => setShowForm(false)}>Cancel</Button>
          </Box>
        </Paper>
      )}

      <Grid container spacing={2}>
        {requirements.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">No requirements yet. Add your first one!</Typography>
          </Box>
        ) : (
          requirements.map((req) => (
            <Grid item xs={12} md={6} key={req.id}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="subtitle2">{req.raw_text}</Typography>
                <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip label="Status: " color="default" />
                </Box>
              </Paper>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
}

export default Requirements;
