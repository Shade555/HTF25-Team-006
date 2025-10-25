import React, { useState } from 'react'
import './dashboard.css'

export default function Dashboard() {
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [podcasts, setPodcasts] = useState([])

  function handleFileChange(e) {
    const files = Array.from(e.target.files || [])
    // Keep only .pdf and .txt files (extra safety)
    const valid = files.filter((f) => /\.pdf$|\.txt$/i.test(f.name))
    setUploadedFiles((prev) => [...prev, ...valid])
  }

  // This simulates generating a podcast — in real app this will call backend.
  function addDemoPodcast() {
    const demo = {
      id: Date.now(),
      title: `Demo podcast ${podcasts.length + 1}`,
      // A small public sample mp3 for testing. Replace with real storage URL later.
      src: 'https://interactive-examples.mdn.mozilla.net/media/examples/t-rex-roar.mp3',
    }
    setPodcasts((p) => [demo, ...p])
  }

  return (
    <main className="dashboard-root">
      <header>
        <h1>Test Dashboard</h1>
        <p className="subtitle">Upload .pdf or .txt files to generate podcast (backend not connected)</p>
      </header>

      <section className="upload-section">
        <h2>Upload File</h2>
        <form
          onSubmit={(e) => {
            e.preventDefault()
            // In the real flow, you'd POST the file to /api/generate-podcast
            alert('This is a test dashboard. Implement backend call to generate podcast.')
          }}
        >
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileChange}
            aria-label="Upload document (PDF or TXT)"
          />
          <div className="uploaded-list">
            <h3>Queued uploads</h3>
            {uploadedFiles.length === 0 && <p>No files selected</p>}
            <ul>
              {uploadedFiles.map((f, i) => (
                <li key={`${f.name}-${i}`}>{f.name}</li>
              ))}
            </ul>
          </div>
          <div className="actions">
            <button type="submit">Simulate Generate</button>
            <button type="button" onClick={addDemoPodcast} className="secondary">
              Add Demo Podcast
            </button>
          </div>
        </form>
      </section>

      <section className="podcasts-section">
        <h2>My Podcasts</h2>
        {podcasts.length === 0 && <p>No podcasts yet. Use "Add Demo Podcast" to test audio players.</p>}
        <ul>
          {podcasts.map((p) => (
            <li key={p.id} className="podcast-item">
              <div className="podcast-meta">
                <strong>{p.title}</strong>
              </div>
              <audio controls src={p.src}>
                Your browser does not support the audio element.
              </audio>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
