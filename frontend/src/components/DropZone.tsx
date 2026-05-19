import { useCallback, useState } from 'react'
import { C } from '../lib/theme'

interface Props {
  onFile: (file: File) => void
}

export default function DropZone({ onFile }: Props) {
  const [dragging, setDragging] = useState(false)

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file?.type === 'application/pdf') onFile(file)
  }, [onFile])

  return (
    <label
      onDragOver={e => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        border: `1.5px dashed ${dragging ? 'var(--accent)' : C.border}`,
        borderRadius: 14,
        padding: '52px 32px',
        cursor: 'pointer',
        background: dragging ? C.accentSub : 'transparent',
        transition: 'all .2s',
      }}
    >
      <input
        type="file"
        accept="application/pdf"
        style={{ display: 'none' }}
        onChange={e => { const f = e.target.files?.[0]; if (f) onFile(f) }}
      />
      <div style={{
        width: 64, height: 64, borderRadius: 16,
        background: C.accentSub, color: C.accent,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        marginBottom: 16,
      }}>
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="12" y1="18" x2="12" y2="12"/>
          <polyline points="9 15 12 12 15 15"/>
        </svg>
      </div>
      <p style={{ fontSize: 16, fontWeight: 600, color: C.t2, margin: '0 0 6px' }}>
        {dragging ? 'Drop it!' : 'Drag & drop your PDF here'}
      </p>
      <p style={{ fontSize: 13, color: C.t4, margin: 0 }}>
        or <span style={{ color: C.accentL }}>browse files</span> · PDF only · max 20 MB
      </p>
    </label>
  )
}
