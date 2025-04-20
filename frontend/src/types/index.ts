export interface File {
  id: number;
  name: string;
  mime_type: string;
  size: number;
  folder_id: number;
  path: string;
  created_at: string;
  updated_at: string;
  download_url: string;
}

export interface Folder {
  id: number;
  name: string;
  path: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface FolderContents extends Folder {
  files: File[];
  subfolders: Folder[];
}

export interface FileUploadResponse {
  id: number;
  name: string;
  path: string;
  mime_type: string;
  size: number;
  folder_id: number;
  created_at: string;
  updated_at: string;
  download_url: string;
}

export interface CreateFolderRequest {
  name: string;
  parent_id: number | null;
}

export interface UpdateFileRequest {
  name?: string;
  folder_id?: number;
}

export interface UpdateFolderRequest {
  name?: string;
  parent_id?: number;
}
