import { useState } from 'react';
import { Upload, File, Loader2, Trash2, CheckCircle } from 'lucide-react';
import { documentsAPI } from '../services/api';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const DocumentUpload = () => {
  const [isDragging, setIsDragging] = useState(false);
  const queryClient = useQueryClient();

  const { data: documents, isLoading } = useQuery({
    queryKey: ['documents'],
    queryFn: documentsAPI.listDocuments,
  });

  const uploadMutation = useMutation({
    mutationFn: documentsAPI.uploadDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: documentsAPI.deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files) {
      Array.from(files).forEach(file => {
        uploadMutation.mutate(file);
      });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Upload className="w-6 h-6" />
        Document Upload
      </h2>

      <div className="border-2 border-dashed rounded-lg p-8 text-center border-gray-300 hover:border-gray-400">
        <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
        <p className="text-sm text-gray-600 mb-2">
          Click to browse files
        </p>
        <p className="text-xs text-gray-500 mb-4">
          Supports PDF and TXT files
        </p>
        <input
          type="file"
          multiple
          accept=".pdf,.txt"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer"
        >
          Select Files
        </label>
      </div>

      {uploadMutation.isPending && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg flex items-center gap-3">
          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          <span className="text-sm text-blue-900">Uploading document...</span>
        </div>
      )}

      {uploadMutation.isSuccess && (
        <div className="mt-4 p-4 bg-green-50 rounded-lg flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-green-600" />
          <span className="text-sm text-green-900">Document uploaded successfully!</span>
        </div>
      )}

      <div className="mt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Uploaded Documents</h3>
        {isLoading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : documents && documents.length > 0 ? (
          <div className="space-y-2">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <div className="flex items-center gap-3">
                  <File className="w-5 h-5 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{doc.filename}</p>
                    <p className="text-xs text-gray-500">
                      {doc.num_chunks} chunks • {doc.file_type.toUpperCase()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => deleteMutation.mutate(doc.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500 text-center py-8">
            No documents uploaded yet
          </p>
        )}
      </div>
    </div>
  );
};
