import React, { useState } from 'react';
import {
  Box, Paper, Typography, TextField, Button, Chip, Container, Grid, Alert, Card, CardContent, Table, TableBody, TableCell, TableRow, MenuItem
} from '@mui/material';

function Estimates() {
  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Estimate User Stories</Typography>
        
        <Alert severity="info" sx={{ mb: 2 }}>
          AI-powered effort estimation for user stories using story points.
        </Alert>

        <Box component="form" sx={{ mt: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Enter User Story Description"
            placeholder="Describe the user story to estimate..."
            variant="outlined"
            sx={{ mb: 2 }}
          />

          <TextField
            select
            fullWidth
            label="Estimation Method"
            value=""
            onChange={() => {}}
            sx={{ mb: 2 }}
          >
            <option value="">Select method...</option>
            <option value="llm">LLM Analysis</option>
            <option value="heuristic">Heuristic Formula</option>
          </TextField>

          <Button variant="contained" color="primary">
            Generate Estimation
          </Button>
        </Box>
      </Paper>

      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell><strong>User Story ID</strong></TableCell>
              <TableCell><strong>Title</strong></TableCell>
              <TableCell><strong>Story Points</strong></TableCell>
              <TableCell><strong>Confidence</strong></TableCell>
              <TableCell><strong>Method</strong></TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Alert severity="success" sx={{ mt: 2 }}>
        Ready to estimate stories. Enter a story description above and click "Generate Estimation".
      </Alert>
    </Container>
  );
}

export default Estimates;
