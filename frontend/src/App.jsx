import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar, Toolbar, Typography, Button, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box,
  IconButton, Avatar, Menu, MenuItem, Divider, Chip
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DescriptionIcon from '@mui/icons-material/Description';
import StoryIcon from '@mui/icons-material/Story';
import AssessmentIcon from '@mui/icons-material/Assessment';
import TestTubeIcon from '@mui/icons-material/TestTube';
import DesignServicesIcon from '@mui/icons-material/DesignServices';
import PuzzleIcon from '@mui/icons-material/Puzzle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LogoutIcon from '@mui/icons-material/Logout';

const drawerWidth = 260;

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogin = () => {
    setUser({ name: 'Demo User', email: 'user@example.com' });
    navigate('/requirements');
  };

  const handleLogout = () => {
    setUser(null);
    navigate('/login');
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const menuItems = [
    { text: 'Requirements', icon: DescriptionIcon, path: '/requirements' },
    { text: 'User Stories', icon: StoryIcon, path: '/stories' },
    { text: 'Estimates', icon: AssessmentIcon, path: '/estimates' },
    { text: 'Test Cases', icon: TestTubeIcon, path: '/test-cases' },
    { text: 'Design Suggestions', icon: DesignServicesIcon, path: '/design' },
    { text: 'Resource Gaps', icon: PuzzleIcon, path: '/resource-gaps' },
    { text: 'Analytics', icon: TrendingUpIcon, path: '/analytics' },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <DashboardIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI SDLC Orchestrator
          </Typography>
          
          {!user ? (
            <Button color="inherit" onClick={() => navigate('/login')}>
              Login
            </Button>
          ) : (
            <>
              <Avatar sx={{ ml: 2, width: 32, height: 32 }} alt={user.name}>
                {user.name.charAt(0)}
              </Avatar>
              <IconButton size="small" onClick={(e) => { e.stopPropagation(); setAnchorEl(e.target); }}>
                <AccountCircleIcon />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
              >
                <MenuItem onClick={() => { handleLogout(); handleMenuClose(); }}>
                  <ListItemIcon><LogoutIcon fontSize="small" /></ListItemIcon>
                  Logout
                </MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </AppBar>
      
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth }
          }}
        >
          <Toolbar>
            <DashboardIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle1" sx={{ flexGrow: 1 }}>SDLC</Typography>
          </Toolbar>
          <Divider />
          <List component="nav">
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton selected={location.pathname === item.path} onClick={() => navigate(item.path)}>
                  <ListItemIcon><item.icon sx={{ color: 'primary.main' }} /></ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Drawer>
      </Box>
      
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        {/* Page content will be rendered here based on routing */}
      </Box>
    </Box>
  );
}

export default App;
