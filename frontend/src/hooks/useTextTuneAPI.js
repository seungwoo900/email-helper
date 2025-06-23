import axios from 'axios'; // HTTP client for making requests
import {useQuery} from '@tanstack/react-query'; // React Query for data fetching and state management

// Bring the analyze function from the backend
// This function will send the text to the backend for analysis
export function useAnalyze(text, options) {
  return useQuery({
    queryKey: ['analyze', text],
    queryFn: async () => {
      const res = await axios.post('/analyze', {text: JSON.stringify(text)})
      console.log('Response from /analyze:', res.data)
      // res.data === { paragraphs: [ { sentences: […] }, … ] }
      return res.data
    },
    staleTime: 5 * 60_000,
    cacheTime: 30 * 60_000,
    ...options,
  })
}