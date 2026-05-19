import { useCallback, useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import DropZone from '../components/DropZone'
import UploadProgress from '../components/UploadProgress'
import { uploadFile, type UploadJob } from '../api/upload'
import { C } from '../lib/theme'

const SOURCES = [
  { value: 'navi', label: 'Navi' },
  { value: 'phonepe', label: 'PhonePe' },
  { value: 'googlepay', label: 'Google Pay' },
]

const TIPS = [
  'Export PDFs directly from the app — Navi, PhonePe, and Google Pay all support in-app statement exports.',
  'Password-protected PDFs must be decrypted before uploading.',
  'Upload one statement per file — separate uploads per month work best.',
  'Transactions are deduplicated automatically, so re-uploading an older statement is safe.',
]

export default function Upload() {
  const qc = useQueryClient()
  const [source, setSource] = useState('navi')
  const [jobId, setJobId] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFile = useCallback(async (file: File) => {
    setError(null)
    setJobId(null)
    setUploading(true)
    try {
      const job = await uploadFile(file, source)
      setJobId(job.id)
    } catch {
      setError('Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }, [source])

  const handleComplete = useCallback((job: UploadJob) => {
    if (job.status === 'completed') {
      qc.invalidateQueries({ queryKey: ['transactions'] })
      qc.invalidateQueries({ queryKey: ['summary'] })
      qc.invalidateQueries({ queryKey: ['byCategory'] })
      qc.invalidateQueries({ queryKey: ['byMonth'] })
      qc.invalidateQueries({ queryKey: ['byDay'] })
      qc.invalidateQueries({ queryKey: ['topMerchants'] })
    }
  }, [qc])

  const cardStyle = {
    background: C.surface,
    border: `1px solid ${C.border}`,
    borderRadius: 14,
    transition: 'background .25s',
  }

  return (
    <div style={{ maxWidth: 620, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div>
        <h1 style={{ fontSize: 24, fontWeight: 700, color: C.t1, margin: '0 0 6px', letterSpacing: '-0.5px' }}>Upload Statement</h1>
        <p style={{ fontSize: 14, color: C.t4, margin: 0 }}>Import your UPI statement PDF to auto-parse transactions.</p>
      </div>

      {/* Source selector */}
      <div style={{ ...cardStyle, padding: '16px 20px' }}>
        <h3 style={{ fontSize: 12, fontWeight: 600, color: C.t4, marginBottom: 12, letterSpacing: '.05em' }}>SELECT APP</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          {SOURCES.map(s => (
            <button
              key={s.value}
              onClick={() => setSource(s.value)}
              style={{
                flex: 1, padding: '9px 0', borderRadius: 10, fontSize: 13, fontWeight: 600,
                border: source === s.value ? `1.5px solid var(--accent)` : `1px solid ${C.border}`,
                background: source === s.value ? C.accentSub : 'transparent',
                color: source === s.value ? C.accentL : C.t3,
                cursor: 'pointer', transition: 'all .15s',
              }}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {!jobId && !uploading && <DropZone onFile={handleFile} />}
      {uploading && <p style={{ fontSize: 13, color: C.t4, textAlign: 'center' }}>Uploading…</p>}
      {error && <p style={{ fontSize: 13, color: '#f87171', textAlign: 'center' }}>{error}</p>}
      {jobId && <UploadProgress jobId={jobId} onComplete={handleComplete} />}

      {jobId && (
        <button
          onClick={() => { setJobId(null); setError(null) }}
          style={{
            padding: '9px 0', fontSize: 13, border: `1px solid ${C.border}`,
            borderRadius: 10, background: 'transparent', color: C.t3, cursor: 'pointer',
          }}
        >
          Upload Another File
        </button>
      )}

      {/* Tips */}
      <div style={{ ...cardStyle, padding: '20px 24px' }}>
        <h3 style={{ fontSize: 12, fontWeight: 600, color: C.t4, marginBottom: 12, letterSpacing: '.05em' }}>TIPS FOR BEST RESULTS</h3>
        {TIPS.map((tip, i) => (
          <div key={i} style={{ display: 'flex', gap: 10, marginBottom: i < TIPS.length - 1 ? 9 : 0, alignItems: 'flex-start' }}>
            <span style={{ color: C.accent, fontSize: 14, marginTop: 1, flexShrink: 0 }}>·</span>
            <span style={{ fontSize: 13, color: C.t4, lineHeight: 1.55 }}>{tip}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
