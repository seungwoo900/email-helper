import { useState } from "react";
import SentenceList from './SentenceList';
import {useAnalyze} from '../hooks/useTextTuneAPI';

export default function Editor() {
    const [text, setText] = useState("");
    const {data, isLoading, refetch} = useAnalyze(text, {enabled: false});

    return (
        <div className="p-4 max-w-2xl mx-auto">
            <textarea
                className="w-full p-2 border rounded mb-3"
                rows="10"
                placeholder="Paste your text here..."
                value={text}
                onChange={e => setText(e.target.value)}
            />

            <button
                className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50" // Change button text based on loading state
                disabled={!text.trim() || isLoading}
                onClick={() => refetch()}
            >
                {isLoading ? "Analyzing..." : "Analyze Text"}
            </button>

            {data && <SentenceList sentences={data.sentences} />}
        </div>
    )
}