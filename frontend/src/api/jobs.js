import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
    }
)

/**
 * Search jobs with filters and pagination
 */
export const searchJobs = async (params = {}) => {
    const { data } = await api.get('/jobs', { params })
    return data
}

/**
 * Get available locations for filtering
 */
export const getJobLocations = async () => {
    const { data } = await api.get('/jobs/locations')
    return data
}

/**
 * Get available experience levels for filtering
 */
export const getExperienceLevels = async () => {
    const { data } = await api.get('/jobs/experience-levels')
    return data
}

/**
 * Get job statistics
 */
export const getJobStats = async () => {
    const { data } = await api.get('/jobs/stats')
    return data
}

export default api
