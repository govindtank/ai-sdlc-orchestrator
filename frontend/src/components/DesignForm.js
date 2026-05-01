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
  Chip,
} from '@mui/material';

const DesignForm = () => {
  const [userStoryId, setUserStoryId] = useState('');
  const [designSuggestion, setDesignSuggestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [userStories, setUserStories] = useState([]);

  useEffect(() => {
    const fetchUserStories = async () => {
      try {
        const response = await axios.get('/api/v1/stories/');
        setUserStories(response.data);
      } catch (err) {
        console.error('Failed to fetch user stories:', err);
      }
    };
    fetchUserStories();
  }, []);

  const handleGenerateDesign = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    setDesignSuggestion(null);
    try {
      const response = await axios.post(
        `/api/v1/design-suggestions/generate-design/${userStoryId}`
      );
      setDesignSuggestion(response.data);
      setSuccess('Design suggestion generated successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to generate design suggestion. Please try again.');
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
      // In a real app, we'd have a form for individual design suggestions
      // For demo, we'll just show a message
      setSuccess('Design suggestion saved successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to save design suggestion. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Design Suggestion Management
      </Typography>
      {error && (
        <Alert severity="error">{error}</Alert>
      )}
      {success && (
        <Alert severity="success">{success}</Alert>
      )}
      <Stack spacing={2}>
        <TextField
          label="Select User Story"
          variant="outlined"
          select
          labelId="user-story-select"
          id="user-story-select"
          value={userStoryId}
          onChange={(e) => setUserStoryId(e.target.value)}
          required
          fullWidth
        >
          <MenuItem value="">
            <em>None selected</em>
          </MenuItem>
          {userStories.map((story) => (
            <MenuItem key={story.id} value={story.id}>
              {story.title.length > 30
                ? story.title.substring(0, 30) + '...'
                : story.title}
            </MenuItem>
          ))}
        </TextField>
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerateDesign}
          disabled={loading || !userStoryId}
          startIcon={loading ? <span>Generating...</span> : null}
        >
          Generate Design Suggestion from User Story
        </Button>

        {designSuggestion ? (
          <Box sx={{ border: '1px solid #ddd', borderRadius: 2, p: 3 }}>
            {designSuggestion.wireframe_description && (
              <>
                <Typography variant="h5" gutterBottom>
                  Wireframe Description
                </Typography>
                <Typography variant="body1">
                  {designSuggestion.wireframe_description}
                </Typography>
              </>
            )}
            {designSuggestion.ui_component_suggestions && designSuggestion.ui_component_suggestions.length > 0 && (
              <>
                <Typography variant="h5" gutterBottom>
                  UI Component Suggestions
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                  {designSuggestion.ui_component_suggestions.map((comp, index) => (
                    <Chip key={index} label={comp} size="small" />
                  ))}
                </Box>
              </>
            )}
            {designSuggestion.design_notes && (
              <>
                <Typography variant="h5" gutterBottom>
                  Design Notes
                </Typography>
                <Typography variant="body1">
                  {designSuggestion.design_notes}
                </Typography>
              </>
            )}
          </Box>
        ) : null}
        
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          onClick={handleSubmit}
          disabled={loading}
          startIcon={loading ? <span>Saving...</span> : null}
        >
          Save Design Suggestion
        </Button>
      </Stack>
    </Container>
  );
};

export default DesignForm;