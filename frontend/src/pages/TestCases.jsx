import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, Typography, TextField, Button, Chip, Container, Grid, Table, TableBody, TableCell, TableRow, MenuItem
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function TestCases() {
  const navigate = useNavigate();
  const [testCases, setTestCases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      // This will call the AI service to generate test cases
      const storyId = prompt('Enter User Story ID:');
      if (!storyId) return;

      setLoading(true);
      // Call backend API - placeholder for actual implementation
      alert(`Generating test cases for user story ${storyId}...`);
    } catch (err) {
      alert('Failed to generate test cases');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Test Cases</Typography>
          <Button variant="contained" onClick={handleGenerate}>
            🤖 Generate Test Cases with AI
          </Button>
        </Box>
      </Paper>

      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell><strong>ID</strong></TableCell>
              <TableCell><strong>Function Name</strong></TableCell>
              <TableCell><strong>Description</strong></TableCell>
              <TableCell><strong>Type</strong></TableCell>
              <TableCell><strong>Status</strong></TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Alert severity="info" sx={{ mt: 2 }}>
        Click "Generate Test Cases with AI" to generate comprehensive test cases for any user story.
      </Alert>
    </Container>
  );
}

export default TestCases;
