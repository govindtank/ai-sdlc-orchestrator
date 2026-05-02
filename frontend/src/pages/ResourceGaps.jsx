import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Paper, Typography, Chip, Container, Grid, Alert, Table, TableBody, TableCell, TableRow, Card, CardContent } from '@mui/material';

function ResourceGaps() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Resource Gap Analysis</Typography>
          <Button variant="contained" color="warning">
            🔍 Run Gap Detection
          </Button>
        </Box>
      </Paper>

      <Alert severity="success" sx={{ mb: 2 }}>
        ✅ AI-powered gap detection identifies missing requirements, design flaws, data issues, API gaps, and assets.
      </Alert>

      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell><strong>ID</strong></TableCell>
              <TableCell><strong>Type</strong></TableCell>
              <TableCell><strong>Description</strong></TableCell>
              <TableCell><strong>Suggested Solution</strong></TableCell>
              <TableCell><strong>Severity</strong></TableCell>
              <TableCell><strong>Status</strong></TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Alert severity="info" sx={{ mt: 2 }}>
        Click "Run Gap Detection" to analyze your project for resource gaps. The AI will detect missing elements and suggest solutions.
      </Alert>
    </Container>
  );
}

export default ResourceGaps;
