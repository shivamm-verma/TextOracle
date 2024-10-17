// // src/components/PdfViewer.jsx
// import React, { useState } from 'react';
// import axios from 'axios';
// import { Box, Typography, Button, TextField, Select, MenuItem, FormControl, InputLabel, Container } from '@mui/material';

// const PdfViewer = () => {
//     const [file, setFile] = useState(null);
//     const [language, setLanguage] = useState('English');
//     const [summary, setSummary] = useState('');
//     const [query, setQuery] = useState('');
//     const [answer, setAnswer] = useState('');

//     const handleFileChange = (e) => {
//         setFile(e.target.files[0]);
//     };

//     const handleLanguageChange = (e) => {
//         setLanguage(e.target.value);
//     };

//     const handleSummarize = async () => {
//         const formData = new FormData();
//         formData.append('file', file);
//         formData.append('language', language);

//         try {
//             const response = await axios.post('http://localhost:8000/pdf/summarize', formData, {
//                 headers: {
//                     'Content-Type': 'multipart/form-data',
//                 },
//             });
//             setSummary(response.data.summary);
//         } catch (error) {
//             console.error('Error summarizing PDF:', error);
//         }
//     };

//     const handleQuery = async () => {
//         const formData = new FormData();
//         formData.append('file', file);
//         formData.append('question', query);
//         formData.append('language', language);

//         try {
//             const response = await axios.post('http://localhost:8000/pdf/query', formData, {
//                 headers: {
//                     'Content-Type': 'multipart/form-data',
//                 },
//             });
//             setAnswer(response.data.answer);
//         } catch (error) {
//             console.error('Error querying PDF:', error);
//         }
//     };

//     return (
//         <Container sx={{ p: 3, backgroundColor: '#000000', color: '#74f0ed' }}>
//             <Typography variant="h4" align="center" gutterBottom>
//                 PDF Viewer
//             </Typography>
//             <Box sx={{ mb: 2 }}>
//                 <input type="file" accept=".pdf" onChange={handleFileChange} />
//             </Box>
//             <FormControl fullWidth sx={{ mb: 2 }} variant="outlined">
//                 <InputLabel id="language-select-label">Select Language</InputLabel>
//                 <Select
//                     labelId="language-select-label"
//                     value={language}
//                     onChange={handleLanguageChange}
//                     label="Select Language"
//                     sx={{ backgroundColor: '#ffffff' }}
//                 >
//                     <MenuItem value="English">English</MenuItem>
//                     <MenuItem value="Spanish">Spanish</MenuItem>
//                     {/* Add more languages as needed */}
//                 </Select>
//             </FormControl>
//             <Button variant="contained" color="secondary" onClick={handleSummarize} sx={{ mb: 2 }}>
//                 Summarize PDF
//             </Button>
//             <Typography variant="h6">Summary:</Typography>
//             <Typography variant="body1" sx={{ whiteSpace: 'pre-line', marginBottom: '20px' }}>
//                 {summary}
//             </Typography>

//             <Typography variant="h6">Ask a question about the PDF:</Typography>
//             <TextField
//                 variant="outlined"
//                 fullWidth
//                 value={query}
//                 onChange={(e) => setQuery(e.target.value)}
//                 sx={{ mb: 2 }}
//                 placeholder="Type your question here..."
//             />
//             <Button variant="contained" color="secondary" onClick={handleQuery}>
//                 Get Answer
//             </Button>
//             <Typography variant="h6" sx={{ marginTop: '20px' }}>Answer:</Typography>
//             <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
//                 {answer}
//             </Typography>
//         </Container>
//     );
// };

// export default PdfViewer;
// src/components/PdfViewer.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, TextField, Select, MenuItem, FormControl, InputLabel, Container } from '@mui/material';

const PdfViewer = () => {
    const [file, setFile] = useState(null);
    const [language, setLanguage] = useState('English');
    const [summary, setSummary] = useState('');
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleLanguageChange = (e) => {
        setLanguage(e.target.value);
    };

    const handleSummarize = async () => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('language', language);

        try {
            const response = await axios.post('http://localhost:8000/pdf/summarize', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSummary(response.data.summary);
        } catch (error) {
            console.error('Error summarizing PDF:', error);
        }
    };

    const handleQuery = async () => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('question', query);
        formData.append('language', language);

        try {
            const response = await axios.post('http://localhost:8000/pdf/query', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setAnswer(response.data.answer);
        } catch (error) {
            console.error('Error querying PDF:', error);
        }
    };

    return (
        <Container sx={{ p: 3, backgroundColor: '#000000', color: '#74f0ed' }}>
            <Typography variant="h4" align="center" gutterBottom>
                PDF Viewer
            </Typography>
            <Box sx={{ mb: 2 }}>
                <input type="file" accept=".pdf" onChange={handleFileChange} />
            </Box>
            <FormControl fullWidth sx={{ mb: 2 }} variant="outlined">
                <InputLabel id="language-select-label">Select Language</InputLabel>
                <Select
                    labelId="language-select-label"
                    value={language}
                    onChange={handleLanguageChange}
                    label="Select Language"
                    sx={{ backgroundColor: '#ffffff' }}
                >
                    <MenuItem value="English">English</MenuItem>
                    <MenuItem value="Spanish">Spanish</MenuItem>
                    {/* Add more languages as needed */}
                </Select>
            </FormControl>
            <Button variant="contained" color="secondary" onClick={handleSummarize} sx={{ mb: 2 }}>
                Summarize PDF
            </Button>
            <Typography variant="h6">Summary:</Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line', marginBottom: '20px' }}>
                {summary}
            </Typography>

            <Typography variant="h6">Ask a question about the PDF:</Typography>
            <TextField
                variant="outlined"
                fullWidth
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="Type your question here..."
            />
            <Button variant="contained" color="secondary" onClick={handleQuery}>
                Get Answer
            </Button>
            <Typography variant="h6" sx={{ marginTop: '20px' }}>Answer:</Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {answer}
            </Typography>
        </Container>
    );
};

export default PdfViewer;
