import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, Button, Card, CardContent, Grid, Paper, CircularProgress } from '@mui/material';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [requirements, setRequirements] = useState([]);
  const [userStories, setUserStories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch projects
        const projectsRes = await axios.get('/api/v1/projects/');
        setProjects(projectsRes.data);
        
        // Fetch requirements
        const reqRes = await axios.get('/api/v1/requirements/');
        setRequirements(reqRes.data);
        
        // Fetch user stories
        const storiesRes = await axios.get('/api/v1/stories/');
        setUserStories(storiesRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
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
          AI SDLC Orchestrator Dashboard
        </Typography>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" align="center" gutterBottom>
        AI SDLC Orchestrator Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Project Overview Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Project Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Total Projects
                  </Typography>
                  <Typography variant="h4">
                    {projects.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Active Projects
                  </Typography>
                  <Typography variant="h4">
                    {projects.filter(p => p.status === 'active').length}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Paper>
        </Grid>
        
        {/* Requirements Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Requirements
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Total Requirements
                  </Typography>
                  <Typography variant="h4">
                    {requirements.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Refined Requirements
                  </Typography>
                  <Typography variant="h4">
                    {requirements.filter(r => r.status === 'refined').length}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Paper>
        </Grid>
        
        {/* User Stories Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                User Stories
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Total Stories
                  </Typography>
                  <Typography variant="h4">
                    {userStories.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Estimated Stories
                  </Typography>
                  <Typography variant="h4">
                    {userStories.filter(s => s.story_points !== null).length}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Paper>
        </Grid>
        
        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Recent Activity
              </Typography>
              {requirements.length > 0 ? (
                <div>
                  {requirements.slice(0, 3).map((req, index) => (
                    <div key={index} style={{ borderBottom: '1px solid #eee', paddingBottom: '8px', marginBottom: '8px' }}>
                      <Typography variant="body1" color="text.primary">
                        {req.raw_text.length > 50 ? req.raw_text.substring(0, 50) + '...' : req.raw_text}
                      </Typography>
                      {req.refined_text ? (
                        <Typography variant="body2" color="text.secondary" style={{ fontStyle: 'italic' }}>
                          Refined: {req.refined_text.length > 50 ? req.refined_text.substring(0, 50) + '...' : req.refined_text}
                        </Typography>
                      ) : (
                        <Typography variant="body2" color="text.warning">
                          Awaiting refinement
                        </Typography>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center">
                  No requirements yet. Start by adding your first requirement!
                </Typography>
              )}
            </CardContent>
          </Paper>
        </Grid>
        
        {/* Action Buttons */}
        <Grid item xs={12}>
          <Grid container justifyContent="center" spacing={2}>
            <Grid item>
              <Button variant="contained" color="primary" size="large">
                Add New Requirement
              </Button>
            </Grid>
            <Grid item>
              <Button variant="outlined" color="secondary" size="large">
                Generate User Stories
              </Button>
            </Grid>
            <Grid item>
              <Button variant="outlined" color="secondary" size="large">
                Estimate Effort
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;