import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useMutation } from "react-query";
import {
  Box,
  Typography,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  Button,
  Alert,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import { uploadFile } from "../../services/api";
import { formatFileSize } from "../../utils/fileUtils";

interface FileUploaderProps {
  folderId: number;
  onUploadComplete: () => void;
}

interface UploadingFile {
  file: File;
  progress: number;
  status: "pending" | "uploading" | "success" | "error";
  error?: string;
}

const FileUploader: React.FC<FileUploaderProps> = ({
  folderId,
  onUploadComplete,
}) => {
  const [files, setFiles] = useState<UploadingFile[]>([]);
  const [overallProgress, setOverallProgress] = useState(0);

  // Upload mutation
  const uploadMutation = useMutation(
    (file: globalThis.File) => uploadFile(folderId, file),
    {
      onSuccess: () => {
        // Update progress
        const completed =
          files.filter((f) => f.status === "success").length + 1;
        const total = files.length;
        setOverallProgress((completed / total) * 100);

        // Check if all files are uploaded
        if (completed === total) {
          onUploadComplete();
        }
      },
    }
  );

  // Handle file drop
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((file) => ({
      file,
      progress: 0,
      status: "pending" as const,
    }));

    setFiles((prev) => [...prev, ...newFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  // Start upload process
  const handleUpload = async () => {
    const pendingFiles = files.filter((f) => f.status === "pending");

    // Update all pending files to uploading
    setFiles((prev) =>
      prev.map((f) =>
        f.status === "pending" ? { ...f, status: "uploading" } : f
      )
    );

    // Upload files one by one
    for (const fileObj of pendingFiles) {
      try {
        await uploadMutation.mutateAsync(fileObj.file);

        // Update file status to success
        setFiles((prev) =>
          prev.map((f) =>
            f.file === fileObj.file
              ? { ...f, status: "success", progress: 100 }
              : f
          )
        );
      } catch (error) {
        // Update file status to error
        setFiles((prev) =>
          prev.map((f) =>
            f.file === fileObj.file
              ? {
                  ...f,
                  status: "error",
                  error:
                    error instanceof Error ? error.message : "Upload failed",
                }
              : f
          )
        );
      }
    }
  };

  // Clear the file list
  const handleClear = () => {
    setFiles([]);
    setOverallProgress(0);
  };

  // Remove a specific file
  const handleRemoveFile = (fileToRemove: File) => {
    setFiles((prev) => prev.filter((f) => f.file !== fileToRemove));
  };

  const hasPendingFiles = files.some((f) => f.status === "pending");
  const hasUploadingFiles = files.some((f) => f.status === "uploading");
  const allFilesProcessed =
    files.length > 0 &&
    files.every((f) => f.status === "success" || f.status === "error");

  return (
    <Box sx={{ width: "100%" }}>
      {/* Dropzone */}
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          textAlign: "center",
          backgroundColor: isDragActive ? "action.hover" : "background.paper",
          border: "2px dashed",
          borderColor: isDragActive ? "primary.main" : "divider",
          borderRadius: 2,
          cursor: "pointer",
          mb: 3,
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
        <Typography variant="h6">
          {isDragActive
            ? "Drop files here"
            : "Drag and drop files here, or click to select files"}
        </Typography>
      </Paper>

      {/* File List */}
      {files.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle1" sx={{ mb: 1 }}>
            Files to upload ({files.length})
          </Typography>

          {/* Overall progress */}
          {(hasUploadingFiles || allFilesProcessed) && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ mb: 0.5 }}>
                Overall Progress: {Math.round(overallProgress)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={overallProgress}
                sx={{ height: 8, borderRadius: 1 }}
              />
            </Box>
          )}

          <List>
            {files.map((fileObj, index) => (
              <ListItem
                key={index}
                secondaryAction={
                  fileObj.status === "pending" && (
                    <Button
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRemoveFile(fileObj.file);
                      }}
                    >
                      Remove
                    </Button>
                  )
                }
              >
                <ListItemIcon>
                  {fileObj.status === "success" ? (
                    <CheckCircleIcon color="success" />
                  ) : fileObj.status === "error" ? (
                    <ErrorIcon color="error" />
                  ) : (
                    <InsertDriveFileIcon />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={fileObj.file.name}
                  secondary={`${formatFileSize(fileObj.file.size)} - ${
                    fileObj.status === "success"
                      ? "Uploaded successfully"
                      : fileObj.status === "error"
                      ? `Error: ${fileObj.error || "Upload failed"}`
                      : fileObj.status === "uploading"
                      ? "Uploading..."
                      : "Pending"
                  }`}
                />
                {fileObj.status === "uploading" && (
                  <Box sx={{ width: "100%", ml: 2 }}>
                    <LinearProgress />
                  </Box>
                )}
              </ListItem>
            ))}
          </List>

          {/* Action buttons */}
          <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
            <Button
              variant="outlined"
              onClick={handleClear}
              sx={{ mr: 2 }}
              disabled={hasUploadingFiles}
            >
              Clear All
            </Button>
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!hasPendingFiles || hasUploadingFiles}
            >
              Upload{" "}
              {hasPendingFiles
                ? `(${files.filter((f) => f.status === "pending").length})`
                : ""}
            </Button>
          </Box>

          {/* Success message */}
          {allFilesProcessed && files.some((f) => f.status === "success") && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {files.filter((f) => f.status === "success").length} file(s)
              uploaded successfully!
            </Alert>
          )}
        </Box>
      )}
    </Box>
  );
};

export default FileUploader;
