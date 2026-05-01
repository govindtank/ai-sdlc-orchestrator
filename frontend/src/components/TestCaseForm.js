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

const TestCaseForm = () => {
  const [userStoryId, setUserStoryId] = useState('');
  const [testCases, setTestCases] = useState([]);
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

  const handleGenerateTests = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const response = await axios.post(
        `/api/v1/test-cases/generate-tests/${userStoryId}`
      );
      setTestCases(response.data);
      setSuccess('Test cases generated successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to generate test cases. Please try again.');
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
      // In a real app, we'd have a form for individual test cases
      // For demo, we'll just show a message
      setSuccess('Test case saved successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to save test case. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Test Case Management
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
          onClick={handleGenerateTests}
          disabled={loading || !userStoryId}
          startIcon={loading ? <span>Generating...</span> : null}
        >
          Generate Test Cases from User Story
        </Button>

        {testCases.length > 0 ? (
          <>
            <Typography variant="h5" gutterBottom>
              Generated Test Cases
            </Typography>
            {testCases.map((tc, index) => (
              <Box key={index} sx={{ border: '1px solid #eee', borderRadius: 2, p: 2, mb: 2 }}>
                <Typography variant="h6" color="primary">
                  Test Case {index + 1}: {tc.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Type: {tc.test_type}
                </Typography>
                <Typography variant="body1">
                  {tc.description}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Steps:
                </Typography>
                <Typography variant="body2">
                  {tc.steps}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Expected Result:
                </Typography>
                <Typography variant="body2">
                  {tc.expected_result}
                </Typography>
              </Box>
            ))}
          </>
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
          Save Test Case
        </Button>
      </Stack>
    </Container>
  );
};

export default TestCaseForm;