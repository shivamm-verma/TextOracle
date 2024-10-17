// src/components/Wikipedia.jsx
import React, { useState } from 'react';
import { summarizeWikipedia, queryWikipedia } from '../api'; // Make sure to implement these functions in api.js

const Wikipedia = () => {
    const [url, setUrl] = useState('');
    const [question, setQuestion] = useState('');
    const [selectedLanguage, setSelectedLanguage] = useState('English');
    const [summary, setSummary] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSummarize = async () => {
        if (!url) {
            alert('Please enter a Wikipedia URL.');
            return;
        }
        const result = await summarizeWikipedia(url, selectedLanguage);
        setSummary(result.summary || 'No summary available.');
    };

    const handleQuery = async () => {
        if (!url || !question) {
            alert('Please enter a Wikipedia URL and a question.');
            return;
        }
        const result = await queryWikipedia(url, question, selectedLanguage);
        setAnswer(result.answer || 'No answer available.');
    };

    return (
        <div>
            <h2>Wikipedia Summarization</h2>
            <input
                type="text"
                placeholder="Enter Wikipedia URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
            />
            {/* <LanguageSelector selectedLanguage={selectedLanguage} setSelectedLanguage={setSelectedLanguage} /> */}
            <button onClick={handleSummarize}>Summarize Article</button>
            <button onClick={handleQuery}>Ask a Question</button>
            <input
                type="text"
                placeholder="Enter your question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />
            <h3>Summary:</h3>
            <p>{summary}</p>
            <h3>Answer:</h3>
            <p>{answer}</p>
        </div>
    );
};

export default Wikipedia;
