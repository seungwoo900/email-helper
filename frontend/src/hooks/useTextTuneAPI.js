import axios from 'axios'; // HTTP client for making requests
import {useQuery, useMutation, useQueryClient} from '@tanstack/react-query';

// Bring the analyze function from the backend
// This function will send the text to the backend for analysis
export function useAnalyze(text, options) {
    return useQuery({
        queryKey: ['analyze', text],
        queryFn: async () => {
            const safeText = JSON.stringify(text)
            const res = await axios.post('/analyze', { text: safeText })
            console.log('Response:', res.data)

            const sentences = res.data.sentences.map(sentence => {
                const raw = sentence.sentence
                let clean
                try {
                    clean = JSON.parse(raw)
                } catch {
                    clean = raw
                }
                return {
                    sentence: clean,
                    difficulty: sentence.difficulty,
                    tone: sentence.tone,
                }
            })
            return {sentences}
        },
        staleTime: 1000 * 60 * 5, // Data is fresh for 5 minutes
        cacheTime: 1000 * 60 * 30, // Data is cached for 30 minutes
        ...options,
    })
}

// Bring the rewrite function from the backend
// This function will send the sentence to the backend for rewriting
// It will return the rewritten sentence
export function useRewrite() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationKey: ['rewrite'],
        mutationFn: async sentence => {
            const res = await axios.post('/rewrite', { sentence })
            return res.data
        },
        onSuccess: () => { // Invalidate the 'analyze' query to refetch data after rewriting
            queryClient.invalidateQueries({ queryKey: ['analyze'] })
        },
    })
}