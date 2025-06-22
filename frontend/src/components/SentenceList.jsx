import SentenceItem from './SentenceItem';

export default function SentenceList({ sentences }) {
    return (
        <div className="mt-6 space-y-2">
            {sentences.map((sentence, index) => ( // Use map to iterate over sentences
                <SentenceItem key={index} sentence={sentence} />
            ))}
        </div>
    )
}