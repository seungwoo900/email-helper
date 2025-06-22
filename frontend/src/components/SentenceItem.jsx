import {useState} from 'react';
import {useRewrite} from '../hooks/useTextTuneAPI';

const bg = {
    easy: 'bg-green-100',
    medium: 'bg-yellow-100',
    hard: 'bg-red-100',
}

export default function SentenceItem({sentence}) {
    const [open, setOpen] = useState(false);
    const {mutate, data: rewritten, isLoading} = useRewrite();

    // If the sentence is clicked, toggle the open state and call mutate with the sentence text
    const toggle = () => {
        if (!open) mutate(sentence.text);
        setOpen(!open);
    }

    return (
        <div>
            <div
                className={`p-4 rounded-lg shadow-md cursor-pointer ${bg[sentence.difficulty]} ${open ? 'mb-4' : 'mb-2'}`}
                onClick={toggle}
            >
                <div className="flex justify-between">
                    <span>{sentence.sentence}</span>
                    <span className="text-sm text-gray-600">
                        {sentence.tone}
                    </span>
                </div>
            </div>
            {open && (                                              // if the item is open
                <div className="ml-4 mt-1 p-2 bg-gray-50 border-l-2 border-blue-400 rounded">
                {isLoading                                   // on loading
                    ? 'Rewritting'                              // show loading text
                    : rewritten?.text || 'Error occurred'             // display rewritten text or error message
                }
                </div>
            )}
        </div>
    )
}