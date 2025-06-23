import React, { useState, useEffect } from "react";
import {useAnalyze} from '../hooks/useTextTuneAPI';
import EmailPreview from "./EmailPreview";

export default function Editor() {
    const [text, setText] = useState("");
    const {data, isLoading, error, refetch} = useAnalyze(text, {enabled: false});
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        let timer
        if (isLoading) {
        setProgress(0)
        timer = setInterval(() => {
            setProgress(prev => {
            const next = prev + Math.random() * 4 // random +0–8%
            return next < 90 ? next : 90
            })
        }, 200) // update every 200 ms
        } else if (progress > 0) {
        // on finish, jump to 100% then reset
        setProgress(100)
        timer = setTimeout(() => setProgress(0), 500)
        }
        return () => clearInterval(timer)
    }, [isLoading])

    return (
        <div className="min-h-screen bg-gray-50 py-10">
            <div className="max-w-7xl mx-auto bg-white shadow-md rounded-lg p-6">
                {/* Title */}
                <h1 className="text-3xl font-bold text-center mb-6">Email Helper</h1>
                {/* Description */}
                <p className="text-center text-gray-600 mb-6">
                Paste your email to automatically refine grammar, tone, and structure.
                </p>


                {/* Split: left for input, right for preview */}
                <div className="flex flex-col lg:flex-row gap-6">
                
                {/* Left pane */}
                <div className="flex-1 flex flex-col">
                    <textarea
                    className="w-full h-80 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                    placeholder="Paste your email here..."
                    value={text}
                    onChange={e => setText(e.target.value)}
                    />

                    <div className="flex justify-center mt-4">
                    <button
                        className="
                        px-6 py-2 bg-blue-600 text-white rounded 
                        hover:bg-blue-700 
                        cursor-pointer disabled:cursor-not-allowed 
                        disabled:opacity-50 transition
                        "
                        disabled={!text.trim() || isLoading}
                        onClick={() => refetch()}
                    >
                        {isLoading ? 'Analyzing…' : 'Analyze Text'}
                    </button>
                    </div>

                    {progress > 0 && (
                    <div className="mt-4">
                        <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
                        <div
                            className="h-2 bg-blue-500 rounded-full transition-all"
                            style={{ width: `${progress}%` }}
                        />
                        </div>
                    </div>
                    )}

                    {error && (
                    <p className="text-red-500 text-center mt-4">{error.message}</p>
                    )}
                </div>

                {/* Right pane */}
                <div className="flex-1 overflow-auto max-h-[60vh]">
                    {data?.paragraphs ? (
                    <EmailPreview paragraphs={data.paragraphs} />
                    ) : (
                    <p className="text-gray-400 italic text-center mt-10">
                        No analysis yet.
                    </p>
                    )}
                </div>
                </div>
            </div>
        </div>
    )
}