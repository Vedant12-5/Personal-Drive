/**
 * Format file size to human-readable format
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * Get file icon based on mime type
 */
export const getFileIcon = (mimeType: string): string => {
  if (!mimeType) return 'description';
  
  if (mimeType.startsWith('image/')) {
    return 'image';
  } else if (mimeType.startsWith('video/')) {
    return 'movie';
  } else if (mimeType.startsWith('audio/')) {
    return 'audiotrack';
  } else if (mimeType === 'application/pdf') {
    return 'picture_as_pdf';
  } else if (mimeType.includes('spreadsheet') || mimeType.includes('excel')) {
    return 'table_chart';
  } else if (mimeType.includes('presentation') || mimeType.includes('powerpoint')) {
    return 'slideshow';
  } else if (mimeType.includes('document') || mimeType.includes('word')) {
    return 'description';
  } else if (mimeType.includes('compressed') || mimeType.includes('zip') || mimeType.includes('tar')) {
    return 'archive';
  } else {
    return 'insert_drive_file';
  }
};

/**
 * Get file extension from filename
 */
export const getFileExtension = (filename: string): string => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
};

/**
 * Check if file is an image
 */
export const isImage = (mimeType: string): boolean => {
  return mimeType.startsWith('image/');
};

/**
 * Check if file is a video
 */
export const isVideo = (mimeType: string): boolean => {
  return mimeType.startsWith('video/');
};

/**
 * Check if file is an audio
 */
export const isAudio = (mimeType: string): boolean => {
  return mimeType.startsWith('audio/');
};

/**
 * Check if file is a PDF
 */
export const isPDF = (mimeType: string): boolean => {
  return mimeType === 'application/pdf';
};
