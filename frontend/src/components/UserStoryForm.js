import React, { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Button,
  TextField,
  Alert,
  Select,
  MenuItem,
  Stack,
  Box,
} from '@mui/material';

const UserStoryForm = () => {
  const [requirementId, setRequirementId] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [acceptanceCriteria, setAcceptanceCriteria] = useState('');
  const [storyPoints, setStoryPoints] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [requirements, setRequirements] = useState([]);

  useEffect(() => {
    const fetchRequirements = async () => {
      try {
        const response = await axios.get('/api/v1/requirements/');
        setRequirements(response.data);
      } catch (err) {
        console.error('Failed to fetch requirements:', err);
      }
    };
    fetchRequirements();
  }, []);

  const handleGenerateStory = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      // Generate user story from requirement
      const response = await axios.post(
        `/api/v1/stories/generate-story/${requirementId}`
      );
      setTitle(response.data.title);
      setDescription(response.data.description);
      // Acceptance criteria might come as a string with bullet points
      setAcceptanceCriteria(response.data.acceptance_criteria || '');
      setSuccess('User story generated successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to generate user story. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleEstimateStory = async () => {
    // This would typically be called after a story is created or selected
    // For simplicity, we'll estimate the current story
    setLoading(true);
    setError('');
    try {
      // In a real app, we'd have a story ID from the generated story
      // For demo, we'll just show a message
      setSuccess('Story estimated: 5 story points (mock)');
    } catch (err) {
      console.error(err);
      setError('Failed to estimate story.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const response = await axios.post('/api/v1/stories/', {
        project_id: 1, // Hardcoded for demo - in real app, this would come from context
        requirement_id: requirementId,
        title,
        description,
        acceptance_criteria: acceptanceCriteria,
        story_points: storyPoints ? parseInt(storyPoints) : null,
      });
      setSuccess('User story created successfully!');
      // Clear form after success
      setTitle('');
      setDescription('');
      setAcceptanceCriteria('');
      setStoryPoints('');
    } catch (err) {
      console.error(err);
      setError('Failed to create user story. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        User Story Management
      </Typography>
      {error && (
        <Alert severity="error">{error}</Alert>
      )}
      {success && (
        <Alert severity="success">{success}</Alert>
      )}
      <Stack spacing={2}>
        <TextField
          label="Select Requirement"
          variant="outlined"
          select
          labelId="requirement-select"
          id="requirement-select"
          value={requirementId}
          onChange={(e) => setRequirementId(e.target.value)}
          required
          fullWidth
        >
          <MenuItem value="">
            <em>None selected</em>
          </MenuItem>
          {requirements.map((req) => (
            <MenuItem key={req.id} value={req.id}>
              {req.raw_text.length > 30
                ? req.raw_text.substring(0, 30) + '...'
                : req.raw_text}
            </MenuItem>
          ))}
        </TextField>
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerateStory}
          disabled={loading || !requirementId}
          startIcon={loading ? <span>Generating...</span> : null}
        >
          Generate User Story from Requirement
        </Button>
        <TextField
          label="Title"
          variant="outlined"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
        />
        <TextField
          label="Description"
          variant="outlined"
          multiline
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          fullWidth
        />
        <TextField
          label="Acceptance Criteria (one per line)"
          variant="outlined"
          multiline
          rows={4}
          value={acceptanceCriteria}
          onChange={(e) => setAcceptanceCriteria(e.target.value)}
          fullWidth
        />
        <TextField
          label="Story Points (optional)"
          variant="outlined"
          type="number"
          value={storyPoints}
          onChange={(e) => setStoryPoints(e.target.value)}
          fullWidth
        />
        <Button
          variant="outlined"
          color="secondary"
          onClick={handleEstimateStory}
          disabled={loading}
          startIcon={loading ? <span>Estimating...</span> : null}
        >
          Estimate Effort
        </Button>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          onClick={handleSubmit}
          disabled={loading}
          startIcon={loading ? <span>Saving...</span> : null}
        >
          Save User Story
        </Button>
      </Stack>
    </Container>
  );
};

export default UserStoryForm;