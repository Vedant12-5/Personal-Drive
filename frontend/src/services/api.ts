import axios from 'axios';
import { 
  File, 
  Folder, 
  FolderContents, 
  CreateFolderRequest, 
  UpdateFileRequest, 
  UpdateFolderRequest,
  FileUploadResponse
} from '../types';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
});

// Folders API
export const getFolders = async (): Promise<Folder[]> => {
  const response = await api.get<Folder[]>('/folders');
  return response.data;
};

export const getFolder = async (id: number): Promise<Folder> => {
  const response = await api.get<Folder>(`/folders/${id}`);
  return response.data;
};

export const getFolderContents = async (id: number): Promise<FolderContents> => {
  const response = await api.get<FolderContents>(`/folders/${id}/contents`);
  return response.data;
};

export const createFolder = async (data: CreateFolderRequest): Promise<Folder> => {
  const response = await api.post<Folder>('/folders', data);
  return response.data;
};

export const updateFolder = async (id: number, data: UpdateFolderRequest): Promise<Folder> => {
  const response = await api.patch<Folder>(`/folders/${id}`, data);
  return response.data;
};

export const deleteFolder = async (id: number): Promise<void> => {
  await api.delete(`/folders/${id}`);
};

// Files API
export const getFile = async (id: number): Promise<File> => {
  const response = await api.get<File>(`/files/${id}`);
  return response.data;
};

export const uploadFile = async (folderId: number, file: globalThis.File): Promise<FileUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<FileUploadResponse>(`/files/upload/?folder_id=${folderId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const updateFile = async (id: number, data: UpdateFileRequest): Promise<File> => {
  const response = await api.patch<File>(`/files/${id}`, data);
  return response.data;
};

export const deleteFile = async (id: number): Promise<void> => {
  await api.delete(`/files/${id}`);
};

// Helper function to get full download URL
export const getDownloadUrl = (downloadUrl: string): string => {
  const baseUrl = process.env.REACT_APP_API_URL || '';
  return `${baseUrl}${downloadUrl}`;
};
