import React from 'react'
import {Clipboard} from 'lucide-react'

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
              <div key={si} className={`${bgClass} p-4 rounded-lg relative group`}>
                {/* Original sentence */}
                <p className="font-medium text-gray-800">{s.original}</p>

                {/* If there’s an edited version, show below */}
                {editedText && (
                  <div className="mt-2">
                    <p className="text-gray-700 dark:text-gray-300 pr-8">
                      {editedText}
                    </p>

                    {/* clipboard button: when group-hover, opacity 100 */}
                    <button
                      onClick={() => navigator.clipboard.writeText(editedText)}
                      aria-label="Copy edited text"
                      className="absolute top-4 right-4 p-1 rounded-full 
                                 opacity-0 group-hover:opacity-100 
                                 transition-opacity cursor-pointer
                                 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <Clipboard size={16} />
                    </button>
                  </div>
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
