import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Paper, Typography, TextField, Button, Chip, Container, Grid, Alert, Card, CardContent, Table, TableBody, TableCell, TableRow
} from '@mui/material';

function DesignSuggestions() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Design Suggestions</Typography>
          <Button variant="contained" color="primary">
            🎨 Generate Wireframe
          </Button>
        </Box>
      </Paper>

      <Alert severity="info" sx={{ mb: 2 }}>
        AI-powered design suggestions including wireframes, UI component recommendations, and design notes.
      </Alert>

      <Card variant="outlined" sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>Add User Story for Design</Typography>
          
          <TextField
            fullWidth
            multiline
            rows={4}
            label="User Story Description"
            placeholder="Describe the feature..."
            variant="outlined"
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="contained" onClick={() => {}}>Generate Design</Button>
            <Button variant="outlined">View Suggestions</Button>
          </Box>
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        {[1, 2].map((_, i) => (
          <Grid item xs={12} md={6} key={i}>
            <Alert severity="default" sx={{ mb: 2 }}>
              📐 Wireframe description would appear here
            </Alert>
            <Alert severity="info">
              💡 UI Component suggestions would appear here
            </Alert>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default DesignSuggestions;
