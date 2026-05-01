import React, { useState, useEffect } from 'react';
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
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  CircularProgress,
} from '@mui/material';

const ResourceGapForm = () => {
  const [projectId, setProjectId] = useState('1'); // Hardcoded for demo
  const [gaps, setGaps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchGaps = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/v1/resource-gaps/?project_id=${projectId}`);
        setGaps(response.data);
      } catch (err) {
        console.error('Failed to fetch resource gaps:', err);
        setError('Failed to load resource gaps.');
      } finally {
        setLoading(false);
      }
    };
    fetchGaps();
  }, [projectId]);

  const handleDetectGaps = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const response = await axios.post(`/api/v1/resource-gaps/detect-gaps/${projectId}`);
      setGaps(response.data);
      setSuccess('Resource gaps detected and saved successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to detect resource gaps. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async (gapId) => {
    // In a real app, we might open a dialog or navigate to a recommendation page
    alert(`Fetching recommendations for gap ${gapId}...`);
    // For now, we'll just log it
    console.log(`Getting recommendations for gap ${gapId}`);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Resource Gap Intelligence
      </Typography>
      {error && (
        <Alert severity="error">{error}</Alert>
      )}
      {success && (
        <Alert severity="success">{success}</Alert>
      )}
      <Stack spacing={2}>
        <TextField
          label="Project ID (for demo)"
          variant="outlined"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          fullWidth
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleDetectGaps}
          disabled={loading}
          startIcon={loading ? <span>Detecting...</span> : null}
        >
          Detect Resource Gaps
        </Button>

        {gaps.length > 0 ? (
          <>
            <Typography variant="h5" gutterBottom>
              Detected Resource Gaps
            </Typography>
            <Paper elevation={3}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Type</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Suggested Solution</TableCell>
                    <TableCell>Severity</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {gaps.map((gap, index) => (
                    <TableRow key={gap.id}>
                      <TableCell>{gap.gap_type}</TableCell>
                      <TableCell>{gap.description}</TableCell>
                      <TableCell>{gap.suggested_solution}</TableCell>
                      <TableCell>
                        <Chip
                          label={gap.severity}
                          size="small"
                          color={gap.severity === 'high' ? 'error' : gap.severity === 'medium' ? 'warning' : 'success'}
                        />
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => handleGetRecommendations(gap.id)}
                        >
                          Recommendations
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          </>
        ) : (
          <Typography variant="body2" color="text.secondary" align="center">
            No resource gaps detected. Click the button above to analyze your project.
          </Typography>
        )}
      </Stack>
    </Container>
  );
};

export default ResourceGapForm;