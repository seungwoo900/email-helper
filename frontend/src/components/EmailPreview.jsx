import React from 'react'

export default function EmailPreview({ paragraphs = [] }) {
  return (
    <div className="space-y-8">
      {paragraphs.map((para, pi) => (
        <div key={pi} className="space-y-4">
          {para.sentences.map((s, si) => {
            const hasSimplified = Boolean(s.simplified)
            const hasCorrected = Boolean(s.corrected)
            // decide which “edited” text to show
            const editedText = hasSimplified
              ? s.simplified
              : hasCorrected
              ? s.corrected
              : null
            // choose background based on type
            const bgClass = hasSimplified
              ? 'bg-yellow-100'
              : hasCorrected
              ? 'bg-red-100'
              : 'bg-green-100'

            return (
              <div key={si} className={`${bgClass} p-4 rounded-lg`}>
                {/* Original sentence */}
                <p className="font-medium text-gray-800">{s.original}</p>

                {/* If there’s an edited version, show below */}
                {editedText && (
                  <p className="mt-2 text-gray-700">
                    {editedText}
                  </p>
                )}

                {/* Reason, if available */}
                {s.reason && (
                  <p className="mt-1 text-sm text-gray-500 italic">
                    Reason: {s.reason}
                  </p>
                )}
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}
