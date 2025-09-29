'use client'
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, FileText, CheckCircle, AlertCircle } from 'lucide-react'

export default function FileUpload({ files, setFiles, onFilesChange }) {
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    const newFiles = [...files, ...acceptedFiles]
    setFiles(newFiles)
    onFilesChange?.(newFiles)

    if (rejectedFiles.length > 0) {
      alert('Some files were rejected. Please upload only PDF, DOCX, or DOC files.')
    }
  }, [files, setFiles, onFilesChange])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
    },
    multiple: true,
    maxSize: 10 * 1024 * 1024 // 10MB
  })

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index)
    setFiles(newFiles)
    onFilesChange?.(newFiles)
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragActive && !isDragReject
            ? 'border-primary-400 bg-primary-50 dark:bg-primary-900/20 scale-105'
            : isDragReject
            ? 'border-red-400 bg-red-50 dark:bg-red-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center transition-all duration-300 ${
            isDragActive 
              ? 'bg-primary-500 text-white animate-bounce' 
              : 'bg-gray-100 dark:bg-gray-800 text-gray-400'
          }`}>
            <Upload className="w-8 h-8" />
          </div>
          
          <div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {isDragActive ? 'Drop files here!' : 'Upload Resume Files'}
            </p>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Drag & drop your PDF, DOCX, or DOC files here, or click to browse
            </p>
            <div className="flex flex-wrap justify-center gap-2 text-xs text-gray-500">
              <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">PDF</span>
              <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">DOCX</span>
              <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">DOC</span>
              <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">Max 10MB</span>
            </div>
          </div>
        </div>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-gray-900 dark:text-white">
              Uploaded Files ({files.length})
            </h4>
            <button
              onClick={() => {
                setFiles([])
                onFilesChange?.([])
              }}
              className="text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Clear All
            </button>
          </div>
          
          <div className="grid gap-2 max-h-60 overflow-y-auto custom-scrollbar">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 group hover:border-primary-300 dark:hover:border-primary-600 transition-colors animate-slide-in-left"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center space-x-3 flex-1 min-w-0">
                  <div className="w-8 h-8 rounded bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
                    <FileText className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <button
                    onClick={() => removeFile(index)}
                    className="w-6 h-6 rounded-full bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800 flex items-center justify-center text-red-600 dark:text-red-400 opacity-0 group-hover:opacity-100 transition-all duration-200"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
