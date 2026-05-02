import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, Typography, TextField, Button, Chip, Container, Grid, Alert, Card, CardContent
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function UserStories() {
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [requirementId, setRequirementId] = useState('');
  const [formData, setFormData] = useState({ title: '', description: '', acceptance_criteria: '' });

  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/stories`);
      setStories(res.data);
    } catch (err) {
      console.error('Failed to load stories:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!requirementId) {
      alert('Please select a requirement ID');
      return;
    }
    try {
      await axios.post(`${API_BASE_URL}/stories`, {
        requirement_id: requirementId,
        ...formData
      });
      fetchStories();
      setFormData({ title: '', description: '', acceptance_criteria: '' });
      setShowForm(false);
      alert('User Story created successfully!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create user story');
    }
  };

  if (loading) return <Typography>Loading user stories...</Typography>;

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">User Stories</Typography>
          <Button variant="contained" onClick={() => setShowForm(true)}>
            + Add New Story
          </Button>
        </Box>
      </Paper>

      {showForm && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Add New User Story</Typography>
          
          <TextField
            select
            fullWidth
            label="Requirement ID"
            value={requirementId}
            onChange={(e) => setRequirementId(e.target.value)}
            sx={{ mb: 2 }}
          >
            {requirementId && <option value={requirementId}>{requirementId}</option>}
          </TextField>

          <TextField
            fullWidth
            multiline
            rows={3}
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            multiline
            rows={4}
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            multiline
            rows={3}
            label="Acceptance Criteria (JSON)"
            value={formData.acceptance_criteria}
            onChange={(e) => setFormData({ ...formData, acceptance_criteria: e.target.value })}
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="contained" onClick={handleCreate}>Create</Button>
            <Button variant="outlined" onClick={() => setShowForm(false)}>Cancel</Button>
          </Box>
        </Paper>
      )}

      <Grid container spacing={2}>
        {stories.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">No user stories yet. Add your first one!</Typography>
          </Box>
        ) : (
          stories.map((story) => (
            <Grid item xs={12} md={6} key={story.id}>
              <Card sx={{ height: 'auto' }}>
                <CardContent>
                  <Typography variant="subtitle2" component="div">
                    {story.title || story.description?.substring(0, 50)}...
                  </Typography>
                  <Typography color="text.secondary" paragraph>
                    {story.description}
                  </Typography>
                  {story.acceptance_criteria && (
                    <Chip label="Acceptance Criteria" size="small" sx={{ mt: 1 }} />
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
}

export default UserStories;
