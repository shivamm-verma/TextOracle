// src/api.js

import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Change to your FastAPI server URL if deployed

// Function to summarize a Wikipedia article
export const summarizeWikipedia = async (url, language) => {
    const response = await axios.post(`${API_URL}/webpage/summarize`, { url, language });
    return response.data;
};

// Function to query a Wikipedia article
export const queryWikipedia = async (url, question, language) => {
    const response = await axios.post(`${API_URL}/webpage/query`, { url, question, language });
    return response.data;
};

// ... Other API functions (PDF and Research Paper)
