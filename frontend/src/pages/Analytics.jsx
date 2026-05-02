import React, { useState } from 'react';
import {
  Box, Paper, Typography, Container, Grid, Card, CardContent, Alert
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Analytics() {
  const [burndownData, setBurndownData] = useState([]);

  // Sample data for demonstration
  const sampleBurndownData = [
    { storyPoints: 120, completedPoints: 0 },
    { storyPoints: 120, completedPoints: 20 },
    { storyPoints: 120, completedPoints: 45 },
    { storyPoints: 120, completedPoints: 70 },
    { storyPoints: 120, completedPoints: 95 },
    { storyPoints: 120, completedPoints: 120 },
  ];

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>SDLC Analytics & Reporting</Typography>
        
        <Grid container spacing={3}>
          {/* Burndown Chart */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6">Sprint Burndown</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={burndownData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="storyPoints" label={{ value: 'Story Points', position: 'insideTop' }} />
                    <YAxis label={{ value: 'Completed Points', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="storyPoints" stroke="#8884d8" name="Remaining Work" />
                    <Line type="monotone" dataKey="completedPoints" stroke="#82ca9d" name="Completed Work" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Velocity Chart */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">Team Velocity</Typography>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={[
                    { sprint: 'Sprint 1', velocity: 30 },
                    { sprint: 'Sprint 2', velocity: 35 },
                    { sprint: 'Sprint 3', velocity: 40 },
                    { sprint: 'Sprint 4', velocity: 42 },
                  ]}>
                    <XAxis dataKey="sprint" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="velocity" stroke="#82ca9d" name="Velocity Points" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Completion Metrics */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card sx={{ textAlign: 'center', height: '100%' }}>
              <CardContent>
                <Typography variant="h4" color="primary">85%</Typography>
                <Typography>Completion Rate</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ textAlign: 'center', height: '100%' }}>
              <CardContent>
                <Typography variant="h4" color="secondary">3.5</Typography>
                <Typography>Avg Story Points/Sprint</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ textAlign: 'center', height: '100%' }}>
              <CardContent>
                <Typography variant="h4" color="error">0</Typography>
                <Typography>Blocked Stories</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Alert severity="info" sx={{ mt: 3 }}>
          Analytics powered by AI to track sprint progress, team velocity, and project completion metrics.
        </Alert>
      </Paper>
    </Container>
  );
}

export default Analytics;
