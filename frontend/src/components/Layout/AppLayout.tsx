import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { 
  Box, 
  CssBaseline, 
  AppBar, 
  Toolbar, 
  Typography, 
  Drawer, 
  Divider,
  IconButton,
  useTheme,
  useMediaQuery
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import FolderNavigation from '../Navigation/FolderNavigation';

const drawerWidth = 240;

const AppLayout: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [open, setOpen] = useState(!isMobile);

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <CssBaseline />
      
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          zIndex: theme.zIndex.drawer + 1,
          backgroundColor: '#1976d2',
          transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          ...(open && {
            width: `calc(100% - ${drawerWidth}px)`,
            marginLeft: `${drawerWidth}px`,
            transition: theme.transitions.create(['width', 'margin'], {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.enteringScreen,
            }),
          }),
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            {open ? <ChevronLeftIcon /> : <MenuIcon />}
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Personal Drive
          </Typography>
        </Toolbar>
      </AppBar>
      
      {/* Sidebar */}
      <Drawer
        variant={isMobile ? "temporary" : "persistent"}
        open={open}
        onClose={isMobile ? handleDrawerToggle : undefined}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto', height: '100%' }}>
          <Typography 
            variant="h6" 
            sx={{ 
              p: 2, 
              fontWeight: 'bold',
              color: theme.palette.primary.main
            }}
          >
            Folders
          </Typography>
          <Divider />
          <FolderNavigation />
        </Box>
      </Drawer>
      
      {/* Main Content */}
      <Box 
        component="main" 
        sx={{ 
          flexGrow: 1, 
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          overflow: 'hidden'
        }}
      >
        <Toolbar />
        <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};

export default AppLayout;
