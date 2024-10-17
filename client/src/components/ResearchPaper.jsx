// src/components/ResearchPaper.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, TextField, Checkbox, FormControlLabel, Container, Paper, CircularProgress } from '@mui/material';

const ResearchPaper = () => {
    const [paperId, setPaperId] = useState('');
    const [summarize, setSummarize] = useState(false);
    const [query, setQuery] = useState('');
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handlePaperIdChange = (e) => {
        setPaperId(e.target.value);
    };

    const handleSummarizeChange = (e) => {
        setSummarize(e.target.checked);
    };

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError('');
        setResponseData(null);

        try {
            const response = await axios.get(`http://localhost:8000/read_research_paper/${paperId}`, {
                params: { summarize, query }
            });
            setResponseData(response.data);
        } catch (error) {
            setError('An error occurred while fetching the research paper.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container sx={{ p: 3, backgroundColor: '#000000', color: '#74f0ed' }}>
            <Typography variant="h4" align="center" gutterBottom>
                Research Paper Reader
            </Typography>
            <TextField
                label="Enter Paper ID"
                variant="outlined"
                fullWidth
                value={paperId}
                onChange={handlePaperIdChange}
                sx={{ mb: 2 }}
            />
            <FormControlLabel
                control={
                    <Checkbox
                        checked={summarize}
                        onChange={handleSummarizeChange}
                        color="secondary"
                    />
                }
                label="Summarize Paper"
            />
            <TextField
                label="Ask a Question (Optional)"
                variant="outlined"
                fullWidth
                value={query}
                onChange={handleQueryChange}
                sx={{ mb: 2 }}
            />
            <Button variant="contained" color="secondary" onClick={handleSubmit} sx={{ mb: 2 }}>
                Read Paper
            </Button>

            {loading && <CircularProgress color="secondary" />}
            {error && <Typography color="error">{error}</Typography>}
            {responseData && (
                <Paper elevation={3} sx={{ p: 2, mt: 3, backgroundColor: '#333', color: '#fff' }}>
                    <Typography variant="h5">Title: {responseData.Title}</Typography>
                    <Typography variant="body1">Authors: {responseData.Authors}</Typography>
                    <Typography variant="body2">Published: {responseData.Published}</Typography>
                    <Typography variant="h6" sx={{ mt: 2 }}>Content:</Typography>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>{responseData.Page_Content}</Typography>
                    {responseData.Summary && (
                        <Box sx={{ mt: 2, p: 2, border: '1px solid #74f0ed', borderRadius: '8px' }}>
                            <Typography variant="h6">Summary:</Typography>
                            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>{responseData.Summary}</Typography>
                        </Box>
                    )}
                    {responseData.Query_Response && (
                        <Box sx={{ mt: 2, p: 2, border: '1px solid #ea445a', borderRadius: '8px' }}>
                            <Typography variant="h6">Query Response:</Typography>
                            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>{responseData.Query_Response}</Typography>
                        </Box>
                    )}
                </Paper>
            )}
        </Container>
    );
};

export default ResearchPaper;
