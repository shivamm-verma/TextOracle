// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import Home from './components/Home';
import PdfViewer from './components/PdfViewer';
import WebPage from './components/WebPage';
import ResearchPaper from './components/ResearchPaper';
import Wikipedia from './components/Wikipedia';

// Define a custom styling for the links
const navLinkStyle = {
    color: '#74f0ed',
    textDecoration: 'none',
    margin: '0 15px',
    fontSize: '16px',
    transition: 'color 0.3s',
};

const App = () => {
    return (
        <Router>
            <AppBar position="static" sx={{ backgroundColor: '#000000' }}>
                <Container maxWidth="lg">
                    <Toolbar>
                        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, color: '#74f0ed', textDecoration: 'none' }}>
                            SmartScholar
                        </Typography>
                        <Link to="/" style={navLinkStyle}>
                            Home
                        </Link>
                        <Link to="/pdf-viewer" style={navLinkStyle}>
                            PDF Uploader
                        </Link>
                        <Link to="/webpage" style={navLinkStyle}>
                            Web Page Summarization
                        </Link>
                        <Link to="/research-paper" style={navLinkStyle}>
                            Research Paper Reader
                        </Link>
                        <Link to="/wikipedia" style={navLinkStyle}>
                            Wikipedia Summarizer
                        </Link>
                        <Button variant="outlined" color="secondary" sx={{ marginLeft: '10px' }}>
                            Login
                        </Button>
                        <Button variant="contained" color="secondary" sx={{ marginLeft: '10px' }}>
                            Sign Up
                        </Button>
                    </Toolbar>
                </Container>
            </AppBar>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/pdf-viewer" element={<PdfViewer />} />
                <Route path="/webpage" element={<WebPage />} />
                <Route path="/research-paper" element={<ResearchPaper />} />
                <Route path="/wikipedia" element={<Wikipedia />} />
            </Routes>
        </Router>
    );
};

export default App;
