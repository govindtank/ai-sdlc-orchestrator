import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Paper,
  CircularProgress,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  Alert,
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AnalyticsPage = () => {
  const [projectOverview, setProjectOverview] = useState(null);
  const [burndownData, setBurndownData] = useState([]);
  const [velocityData, setVelocityData] = useState([]);
  const [gapTrends, setGapTrends] = useState({});
  const [aiStats, setAiStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // For demo, we assume project ID 1. In a real app, we would get this from context or URL.
        const projectId = 1;

        const [overviewRes, burndownRes, velocityRes, gapTrendsRes, aiStatsRes] = await Promise.all([
          axios.get(`/api/v1/analytics/project/${projectId}/overview`),
          axios.get(`/api/v1/analytics/project/${projectId}/burndown?days=14`),
          axios.get(`/api/v1/analytics/project/${projectId}/velocity?sprints=6`),
          axios.get(`/api/v1/analytics/project/${projectId}/gap-trends`),
          axios.get(`/api/v1/analytics/project/${projectId}/ai-stats`),
        ]);

        setProjectOverview(overviewRes.data);
        setBurndownData(burndownRes.data);
        setVelocityData(velocityRes.data);
        setGapTrends(gapTrendsRes.data);
        setAiStats(aiStatsRes.data);
      } catch (err) {
        console.error('Error fetching analytics data:', err);
        setError('Failed to load analytics data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Typography variant="h4" align="center" gutterBottom>
          Analytics Dashboard
        </Typography>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Typography variant="h4" align="center" gutterBottom>
          Analytics Dashboard
        </Typography>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" align="center" gutterBottom>
        Analytics Dashboard
      </Typography>
      {projectOverview ? (
        <>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Project Overview
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Project Name
                  </Typography>
                  <Typography variant="h4">
                    {projectOverview.project?.name || 'N/A'}
                  </Typography>
                </CardContent>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Requirements
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Total
                      </Typography>
                      <Typography variant="h4">
                        {projectOverview.requirements?.total || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Refined
                      </Typography>
                      <Typography variant="h4">
                        {projectOverview.requirements?.refined || 0}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    User Stories
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Total
                      </Typography>
                      <Typography variant="h4">
                        {projectOverview.user_stories?.total || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Estimated
                      </Typography>
                      <Typography variant="h4">
                        {projectOverview.user_stories?.estimated || 0}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Estimated Effort
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Story Points
                  </Typography>
                  <Typography variant="h4">
                    {projectOverview.estimated_total_story_points?.toFixed(1) || '0'}
                  </Typography>
                </CardContent>
              </Paper>
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Burndown Chart (Last 14 Days)
                  </Typography>
                  {burndownData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={burndownData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" tickFormatter={(date) => new Date(date).toLocaleDateString()} />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="remaining_story_points" stroke="#ff6384" name="Remaining" />
                        <Line type="monotone" dataKey="completed_story_points" stroke="#36a2eb" name="Completed" />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <Typography variant="body2" color="text.secondary" align="center">
                      No burndown data available
                    </Typography>
                  )}
                </CardContent>
              </Paper>
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={6}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Velocity Chart (Last 6 Sprints)
                  </Typography>
                  {velocityData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={velocityData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="sprint" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="story_points_completed" stroke="#4caf50" name="Completed" />
                        <Line type="monotone" dataKey="story_points_committed" stroke="#ff9800" name="Committed" />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <Typography variant="body2" color="text.secondary" align="center">
                      No velocity data available
                    </Typography>
                  )}
                </CardContent>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <Paper elevation={3}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Resource Gap Trends
                  </Typography>
                  {Object.keys(gapTrends).length > 0 ? (
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Gap Type</TableCell>
                          <TableCell>Total</TableCell>
                          <TableCell>Open</TableCell>
                          <TableCell>Resolved</TableCell>
                          <TableCell>Resolution Rate</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {Object.entries(gapTrends).map(([type, data]) => (
                          <TableRow key={type}>
                            <TableCell>{type}</TableCell>
                            <TableCell>{data.total || 0}</TableCell>
                            <TableCell>{data.open || 0}</TableCell>
                            <TableCell>{data.resolved || 0}</TableCell>
                            <TableCell>
                              <Chip
                                label={`${(data.resolution_rate || 0).toFixed(1)}%`}
                                size="small"
                                color={(data.resolution_rate || 0) >= 80 ? 'success' : (data.resolution_rate || 0) >= 50 ? 'warning' : 'error'}
                              />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  ) : (
                    <Typography variant="body2" color="text.secondary" align="center">
                      No resource gap data available
                    </Typography>
                  )}
                </CardContent>
              </Paper>
            </Grid>
          </Grid>

          {aiStats && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper elevation={3}>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      AI Usage Statistics
                    </Typography>
                    <Grid container spacing={3}>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          Total AI Calls
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.total_ai_calls || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          Requirement Refinements
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.requirement_refinements || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          User Story Generations
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.user_story_generations || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          Design Suggestions
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.design_suggestions || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          Test Case Generations
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.test_case_generations || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="body2" color="text.secondary">
                          Effort Estimations
                        </Typography>
                        <Typography variant="h4">
                          {aiStats.effort_estimations || 0}
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Paper>
              </Grid>
            </Grid>
          )}
        </>
      ) : (
        <Typography variant="body2" color="text.secondary" align="center">
          No project data available. Please create a project first.
        </Typography>
      )}
    </Container>
  );
};

export default AnalyticsPage;