import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText,
  Collapse,
  CircularProgress,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { getFolders, createFolder } from '../../services/api';

const FolderNavigation: React.FC = () => {
  const navigate = useNavigate();
  const { folderId } = useParams<{ folderId: string }>();
  const [open, setOpen] = useState<Record<number, boolean>>({});
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');
  
  // Fetch root folders
  const { data: folders, isLoading, refetch } = useQuery('rootFolders', getFolders);
  
  const handleFolderClick = (id: number) => {
    navigate(`/folders/${id}`);
  };
  
  const toggleFolder = (id: number) => {
    setOpen(prev => ({ ...prev, [id]: !prev[id] }));
  };
  
  const handleCreateFolder = async () => {
    if (newFolderName.trim()) {
      await createFolder({ name: newFolderName, parent_id: null });
      setNewFolderName('');
      setIsCreateDialogOpen(false);
      refetch();
    }
  };
  
  if (isLoading) {
    return <CircularProgress />;
  }
  
  return (
    <>
      <List>
        {folders?.map((folder) => (
          <React.Fragment key={folder.id}>
            <ListItem disablePadding>
              <ListItemButton 
                onClick={() => handleFolderClick(folder.id)}
                selected={folderId === folder.id.toString()}
                sx={{ pl: 2 }}
              >
                <ListItemIcon>
                  {folderId === folder.id.toString() ? <FolderOpenIcon color="primary" /> : <FolderIcon />}
                </ListItemIcon>
                <ListItemText primary={folder.name} />
                {/* If we had subfolders, we would add expand/collapse here */}
              </ListItemButton>
            </ListItem>
            {/* Subfolder rendering would go here */}
          </React.Fragment>
        ))}
        
        <ListItem disablePadding>
          <ListItemButton onClick={() => setIsCreateDialogOpen(true)}>
            <ListItemIcon>
              <CreateNewFolderIcon color="primary" />
            </ListItemIcon>
            <ListItemText primary="Create New Folder" />
          </ListItemButton>
        </ListItem>
      </List>
      
      {/* Create Folder Dialog */}
      <Dialog open={isCreateDialogOpen} onClose={() => setIsCreateDialogOpen(false)}>
        <DialogTitle>Create New Folder</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Folder Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsCreateDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateFolder} variant="contained">Create</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FolderNavigation;
