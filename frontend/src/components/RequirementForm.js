import React, { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Button,
  TextField,
  Alert,
  Stack,
  Box,
} from '@mui/material';

const RequirementForm = () => {
  const [rawText, setRawText] = useState('');
  const [refinedText, setRefinedText] = useState('');
  const [clarificationQuestions, setClarificationQuestions] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      // Create the requirement
      const response = await axios.post('/api/v1/requirements/', {
        raw_text: rawText,
      });
      const requirementId = response.data.id;

      // Optionally, refine immediately
      if (rawText.trim()) {
        const refineResponse = await axios.post(
          `/api/v1/requirements/${requirementId}/refine`
        );
        setRefinedText(refineResponse.data.refined_text || '');
        setClarificationQuestions(
          refineResponse.data.clarification_questions || ''
        );
      }

      setSuccess('Requirement created and refined successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to create requirement. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Requirement Management
      </Typography>
      {error && (
        <Alert severity="error">{error}</Alert>
      )}
      {success && (
        <Alert severity="success">{success}</Alert>
      )}
      <form onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <TextField
          label="Raw Requirement"
          variant="outlined"
          multiline
          rows={4}
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          required
          fullWidth
          sx={{ mb: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          disabled={loading}
          startIcon={loading ? <span>Processing...</span> : null}
        >
          Create and Refine Requirement
        </Button>
      </form>

      {refinedText || clarificationQuestions ? (
        <Box sx={{ border: '1px solid #ddd', borderRadius: 2, p: 3 }}>
          {refinedText && (
            <>
              <Typography variant="h5" gutterBottom>
                Refined Requirement
              </Typography>
              <Typography variant="body1">{refinedText}</Typography>
            </>
          )}
          {clarificationQuestions && (
            <>
              <Typography variant="h5" gutterBottom>
                Clarification Questions
              </Typography>
              <Typography variant="body1">
                {clarificationQuestions}
              </Typography>
            </>
          )}
        </Box>
      ) : null}
    </Container>
  );
};

export default RequirementForm;