import React, { useState } from 'react';
import { Upload, FileText, CheckCircle2, XCircle, FileIcon } from 'lucide-react';

const CircularProgress = ({ score }) => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = "text-red-500";
  if (score >= 80) colorClass = "text-green-500";
  else if (score >= 50) colorClass = "text-yellow-500";

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="w-32 h-32 transform -rotate-90">
        <circle
          className="text-gray-200"
          strokeWidth="8"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="64"
          cy="64"
        />
        <circle
          className={`transition-all duration-1000 ease-out ${colorClass}`}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="64"
          cy="64"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-gray-800">{score}</span>
        <span className="text-xs text-gray-500 font-medium">SCORE</span>
      </div>
    </div>
  );
};

const SkeletonLoader = () => (
  <div className="w-full max-w-4xl mx-auto bg-white rounded-3xl shadow-lg p-8 animate-pulse mt-8 border border-gray-100">
    <div className="flex flex-col md:flex-row gap-12 items-center">
      <div className="w-32 h-32 bg-gray-200 rounded-full shrink-0"></div>
      <div className="flex-1 w-full space-y-6">
        <div className="h-6 bg-gray-200 rounded w-1/4"></div>
        <div className="h-4 bg-gray-200 rounded w-full"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        <div className="flex gap-4">
          <div className="h-8 bg-gray-200 rounded-full w-24"></div>
          <div className="h-8 bg-gray-200 rounded-full w-32"></div>
        </div>
        <div className="h-24 bg-gray-100 rounded-xl w-full mt-4"></div>
      </div>
    </div>
  </div>
);

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jobDescription.trim()) {
      setError("Please provide both a resume PDF and a job description.");
      return;
    }

    setError('');
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload/process-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Processing failed');
      }

      const data = await response.json();
      setResult(data.evaluation);
    } catch (err) {
      setError('An error occurred while evaluating the candidate. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-3">
          AI Recruitment Agent
        </h1>
        <p className="text-lg text-gray-600 font-light">
          Upload a resume and job description to get an evidence-based match analysis.
        </p>
      </div>

      {/* Main Input Card */}
      <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-xl p-8 sm:p-12 border border-gray-100">
        <form onSubmit={handleSubmit} className="space-y-10">
          
          {/* File Upload Section */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">Candidate Resume (PDF)</label>
            <div className="mt-1 flex justify-center px-6 pt-8 pb-10 border-2 border-gray-300 border-dashed rounded-2xl hover:border-primary-500 hover:bg-primary-50 transition-colors duration-200 bg-gray-50 relative group cursor-pointer" onClick={() => document.getElementById('file-upload').click()}>
              <div className="space-y-2 text-center flex flex-col items-center">
                {file ? (
                  <>
                    <FileIcon className="mx-auto h-12 w-12 text-primary-500" />
                    <div className="text-sm font-medium text-gray-900">{file.name}</div>
                    <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </>
                ) : (
                  <>
                    <Upload className="mx-auto h-12 w-12 text-gray-400 group-hover:text-primary-500 transition-colors" />
                    <div className="flex text-sm text-gray-600 mt-4">
                      <span className="relative cursor-pointer rounded-md font-medium text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 hover:text-primary-500">
                        <span>Upload a file</span>
                        <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".pdf" onChange={handleFileChange} />
                      </span>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs text-gray-500">PDF up to 10MB</p>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Job Description Text Area (Floating Label) */}
          <div className="relative pt-2">
            <textarea
              id="job_desc"
              className="floating-label-input peer block w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white transition-all duration-200 min-h-[160px] resize-y placeholder-transparent"
              placeholder="Paste job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            ></textarea>
            <label 
              htmlFor="job_desc" 
              className="absolute left-4 top-6 text-gray-500 text-base transition-all duration-200 transform origin-left peer-focus:-translate-y-6 peer-focus:scale-75 peer-focus:text-primary-600 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 cursor-text pointer-events-none"
            >
              Paste Job Description
            </label>
          </div>

          {error && <div className="text-red-500 text-sm font-medium bg-red-50 p-4 rounded-lg flex items-center gap-2"><XCircle className="w-5 h-5"/> {error}</div>}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-4 px-6 border border-transparent rounded-xl shadow-sm text-lg font-medium text-white bg-gray-900 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 transition-all duration-200 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? 'Analyzing Candidate...' : 'Analyze Candidate Match'}
          </button>
        </form>
      </div>

      {/* Loading State */}
      {loading && <SkeletonLoader />}

      {/* Results Card */}
      {result && !loading && (
        <div className="max-w-4xl mx-auto mt-12 bg-white rounded-3xl shadow-xl p-8 sm:p-12 border border-gray-100 animate-in fade-in slide-in-from-bottom-8 duration-500">
          <div className="flex flex-col md:flex-row gap-12 items-start md:items-center mb-10 border-b border-gray-100 pb-10">
            
            <div className="flex-shrink-0 mx-auto md:mx-0">
              <CircularProgress score={result.match_score} />
            </div>

            <div className="flex-1 space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 tracking-tight">Agent Reasoning</h2>
              <div className="bg-gray-50 rounded-2xl p-6 border border-gray-200 font-mono text-sm leading-relaxed text-gray-700 shadow-inner">
                {result.reasoning}
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Matched Skills */}
            <div className="space-y-5">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-green-500" />
                Matched Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.matched_skills?.length > 0 ? (
                  result.matched_skills.map((skill, idx) => (
                    <span key={idx} className="inline-flex items-center px-3.5 py-1.5 rounded-full text-sm font-medium bg-green-50 text-green-700 border border-green-200 shadow-sm transition-transform hover:scale-105">
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-gray-500 italic">No exact matches found.</span>
                )}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="space-y-5">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <XCircle className="w-5 h-5 text-red-500" />
                Missing Core Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.missing_skills?.length > 0 ? (
                  result.missing_skills.map((skill, idx) => (
                    <span key={idx} className="inline-flex items-center px-3.5 py-1.5 rounded-full text-sm font-medium bg-red-50 text-red-700 border border-red-200 shadow-sm transition-transform hover:scale-105">
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-gray-500 italic">Candidate appears to have all core skills.</span>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
