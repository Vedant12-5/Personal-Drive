import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Paper,
  IconButton,
  Menu,
  MenuItem,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Breadcrumbs,
  Link,
  Divider
} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { getFolderContents, createFolder, deleteFolder, deleteFile, updateFolder, updateFile } from '../../services/api';
import { formatFileSize } from '../../utils/fileUtils';
import FileUploader from './FileUploader';

const FileList: React.FC = () => {
  const { folderId } = useParams<{ folderId: string }>();
  const queryClient = useQueryClient();
  const currentFolderId = folderId ? parseInt(folderId) : null;
  
  // State for context menu
  const [contextMenu, setContextMenu] = useState<{
    mouseX: number;
    mouseY: number;
    type: 'file' | 'folder';
    id: number;
    name: string;
  } | null>(null);
  
  // State for dialogs
  const [isCreateFolderDialogOpen, setIsCreateFolderDialogOpen] = useState(false);
  const [isRenameDialogOpen, setIsRenameDialogOpen] = useState(false);
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);
  const [newName, setNewName] = useState('');
  
  // Fetch folder contents
  const { data, isLoading, error } = useQuery(
    ['folderContents', currentFolderId],
    () => currentFolderId ? getFolderContents(currentFolderId) : null,
    { enabled: !!currentFolderId }
  );
  
  // Mutations
  const createFolderMutation = useMutation(createFolder, {
    onSuccess: () => {
      queryClient.invalidateQueries(['folderContents', currentFolderId]);
    },
  });
  
  const deleteFolderMutation = useMutation(deleteFolder, {
    onSuccess: () => {
      queryClient.invalidateQueries(['folderContents', currentFolderId]);
    },
  });
  
  const deleteFileMutation = useMutation(deleteFile, {
    onSuccess: () => {
      queryClient.invalidateQueries(['folderContents', currentFolderId]);
    },
  });
  
  const renameFolderMutation = useMutation(
    ({ id, name }: { id: number; name: string }) => updateFolder(id, { name }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['folderContents', currentFolderId]);
      },
    }
  );
  
  const renameFileMutation = useMutation(
    ({ id, name }: { id: number; name: string }) => updateFile(id, { name }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['folderContents', currentFolderId]);
      },
    }
  );
  
  // Handle context menu
  const handleContextMenu = (event: React.MouseEvent, type: 'file' | 'folder', id: number, name: string) => {
    event.preventDefault();
    setContextMenu({
      mouseX: event.clientX - 2,
      mouseY: event.clientY - 4,
      type,
      id,
      name,
    });
  };
  
  const handleContextMenuClose = () => {
    setContextMenu(null);
  };
  
  // Handle create folder
  const handleCreateFolder = async () => {
    if (newName.trim() && currentFolderId) {
      await createFolderMutation.mutateAsync({
        name: newName,
        parent_id: currentFolderId,
      });
      setNewName('');
      setIsCreateFolderDialogOpen(false);
    }
  };
  
  // Handle rename
  const handleRename = async () => {
    if (newName.trim() && contextMenu) {
      if (contextMenu.type === 'folder') {
        await renameFolderMutation.mutateAsync({
          id: contextMenu.id,
          name: newName,
        });
      } else {
        await renameFileMutation.mutateAsync({
          id: contextMenu.id,
          name: newName,
        });
      }
      setNewName('');
      setIsRenameDialogOpen(false);
    }
  };
  
  // Handle delete
  const handleDelete = async () => {
    if (contextMenu) {
      if (contextMenu.type === 'folder') {
        await deleteFolderMutation.mutateAsync(contextMenu.id);
      } else {
        await deleteFileMutation.mutateAsync(contextMenu.id);
      }
      handleContextMenuClose();
    }
  };
  
  // Handle file download
  const handleFileDownload = (downloadUrl: string) => {
    // Check if the URL is relative or absolute
    if (downloadUrl.startsWith('/')) {
      // Construct the full URL to the backend
      const backendUrl = 'http://localhost:8000';
      const fullUrl = `${backendUrl}${downloadUrl}`;
      console.log('Opening file URL:', fullUrl);
      window.open(fullUrl, '_blank');
    } else {
      // URL is already absolute
      console.log('Opening file URL:', downloadUrl);
      window.open(downloadUrl, '_blank');
    }
  };
  
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">Error loading folder contents</Typography>
      </Box>
    );
  }
  
  if (!data && currentFolderId) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Folder not found</Typography>
      </Box>
    );
  }
  
  // If no folder is selected (root view)
  if (!currentFolderId) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h5">Welcome to Personal Drive</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          Select a folder from the sidebar to view its contents.
        </Typography>
      </Box>
    );
  }
  
  return (
    <Box sx={{ p: 2 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs 
        separator={<NavigateNextIcon fontSize="small" />} 
        aria-label="breadcrumb"
        sx={{ mb: 3 }}
      >
        <Link 
          color="inherit" 
          href="#" 
          onClick={(e) => {
            e.preventDefault();
            // Navigate to parent folder logic would go here
          }}
        >
          Home
        </Link>
        <Typography color="text.primary">{data?.name}</Typography>
      </Breadcrumbs>
      
      {/* Action buttons */}
      <Box sx={{ display: 'flex', mb: 2 }}>
        <Button
          variant="contained"
          startIcon={<CreateNewFolderIcon />}
          onClick={() => setIsCreateFolderDialogOpen(true)}
          sx={{ mr: 2 }}
        >
          New Folder
        </Button>
        <Button
          variant="contained"
          startIcon={<CloudUploadIcon />}
          onClick={() => setIsUploadDialogOpen(true)}
        >
          Upload Files
        </Button>
      </Box>
      
      <Divider sx={{ my: 2 }} />
      
      {/* Folders */}
      {data?.subfolders && data.subfolders.length > 0 && (
        <>
          <Typography variant="h6" sx={{ mb: 1 }}>Folders</Typography>
          <Grid container spacing={2}>
            {data.subfolders.map((folder) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={folder.id}>
                <Paper
                  elevation={2}
                  sx={{
                    p: 2,
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'action.hover' },
                  }}
                  onClick={() => window.location.href = `/folders/${folder.id}`}
                  onContextMenu={(e) => handleContextMenu(e, 'folder', folder.id, folder.name)}
                >
                  <FolderIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
                  <Box sx={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Typography noWrap>{folder.name}</Typography>
                  </Box>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleContextMenu(e, 'folder', folder.id, folder.name);
                    }}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Paper>
              </Grid>
            ))}
          </Grid>
          <Divider sx={{ my: 2 }} />
        </>
      )}
      
      {/* Files */}
      {data?.files && data.files.length > 0 && (
        <>
          <Typography variant="h6" sx={{ mb: 1 }}>Files</Typography>
          <Grid container spacing={2}>
            {data.files.map((file) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={file.id}>
                <Paper
                  elevation={2}
                  sx={{
                    p: 2,
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'action.hover' },
                  }}
                  onClick={() => handleFileDownload(file.download_url)}
                  onContextMenu={(e) => handleContextMenu(e, 'file', file.id, file.name)}
                >
                  <InsertDriveFileIcon color="info" sx={{ fontSize: 40, mr: 2 }} />
                  <Box sx={{ flexGrow: 1, overflow: 'hidden' }}>
                    <Typography noWrap>{file.name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {formatFileSize(file.size)}
                    </Typography>
                  </Box>
                  <Box>
                    <IconButton
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleContextMenu(e, 'file', file.id, file.name);
                      }}
                    >
                      <MoreVertIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleFileDownload(file.download_url);
                      }}
                    >
                      <CloudDownloadIcon />
                    </IconButton>
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </>
      )}
      
      {/* Empty state */}
      {(!data?.subfolders || data.subfolders.length === 0) && 
       (!data?.files || data.files.length === 0) && (
        <Box sx={{ textAlign: 'center', py: 5 }}>
          <Typography variant="h6" color="text.secondary">
            This folder is empty
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Upload files or create folders to get started
          </Typography>
        </Box>
      )}
      
      {/* Context Menu */}
      <Menu
        open={contextMenu !== null}
        onClose={handleContextMenuClose}
        anchorReference="anchorPosition"
        anchorPosition={
          contextMenu !== null
            ? { top: contextMenu.mouseY, left: contextMenu.mouseX }
            : undefined
        }
      >
        <MenuItem
          onClick={() => {
            setNewName(contextMenu?.name || '');
            setIsRenameDialogOpen(true);
            handleContextMenuClose();
          }}
        >
          Rename
        </MenuItem>
        <MenuItem onClick={handleDelete}>Delete</MenuItem>
      </Menu>
      
      {/* Create Folder Dialog */}
      <Dialog open={isCreateFolderDialogOpen} onClose={() => setIsCreateFolderDialogOpen(false)}>
        <DialogTitle>Create New Folder</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Folder Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsCreateFolderDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateFolder} variant="contained">Create</Button>
        </DialogActions>
      </Dialog>
      
      {/* Rename Dialog */}
      <Dialog open={isRenameDialogOpen} onClose={() => setIsRenameDialogOpen(false)}>
        <DialogTitle>Rename {contextMenu?.type === 'folder' ? 'Folder' : 'File'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="New Name"
            type="text"
            fullWidth
            variant="outlined"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsRenameDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleRename} variant="contained">Rename</Button>
        </DialogActions>
      </Dialog>
      
      {/* Upload Dialog */}
      <Dialog 
        open={isUploadDialogOpen} 
        onClose={() => setIsUploadDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Upload Files</DialogTitle>
        <DialogContent>
          <FileUploader 
            folderId={currentFolderId} 
            onUploadComplete={() => {
              setIsUploadDialogOpen(false);
              queryClient.invalidateQueries(['folderContents', currentFolderId]);
            }} 
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsUploadDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FileList;
