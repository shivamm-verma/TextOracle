import React from "react";
import { Grid, Typography, Button, Paper, Box } from "@mui/material";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf"; // For PDF Viewer
import PublicIcon from "@mui/icons-material/Public";// For Wikipedia
import InsightsIcon from "@mui/icons-material/Insights"; // For WebPage Insights
import ArticleIcon from "@mui/icons-material/Article"; // For Research Paper
import { styled } from "@mui/system";
import { useNavigate } from "react-router-dom"; // Import useNavigate instead of useHistory

// Styled component for the Paper container
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  color: theme.palette.text.secondary,
  background: 'linear-gradient(135deg, #1e1e1e, #2a2a2a)', // Gradient for depth
  borderRadius: '15px',
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.5)', // Soft shadow
  transition: 'transform 0.3s, box-shadow 0.3s',
  '&:hover': {
    transform: 'scale(1.03)',
    boxShadow: '0 8px 40px rgba(0, 233, 255, 0.5)', // Light cyan shadow on hover
  },
}));

const Home = () => {
  const navigate = useNavigate(); // Use useNavigate

  return (
    <Box sx={{ flexGrow: 1, p: 3, backgroundColor: "#000000" }}>
      <Typography variant="h3" align="center" gutterBottom sx={{ color: "#74f0ed" }}>
        Welcome to The Concluder
      </Typography>
      <Typography variant="h5" align="center" sx={{ color: "#b0b0b0" }}>
        Your intelligent conculder (PDF, WebPage, Research papers etc.)
      </Typography>

      <Grid container spacing={4} sx={{ mt: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <StyledPaper>
            <PictureAsPdfIcon fontSize="large" sx={{ color: "#74f0ed" }} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              PDF Viewer
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              View your PDF files directly within the application.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => navigate('/pdf-viewer')} sx={{ mt: 2 }}>
              Open PDF Viewer
            </Button>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <StyledPaper>
            <PublicIcon fontSize="large" sx={{ color: "#74f0ed" }} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Wikipedia Insights
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Get summaries and insights from Wikipedia articles.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => navigate('/wikipedia')} sx={{ mt: 2 }}>
              Search Wikipedia
            </Button>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <StyledPaper>
            <InsightsIcon fontSize="large" sx={{ color: "#74f0ed" }} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              WebPage Summarizer
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Analyze webpages for key information and insights.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => navigate('/webpage-summarizer')} sx={{ mt: 2 }}>
              Analyze Webpage
            </Button>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <StyledPaper>
            <ArticleIcon fontSize="large" sx={{ color: "#74f0ed" }} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Research Assistant
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Upload your research papers for analysis and summarization.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => navigate('/research-paper')} sx={{ mt: 2 }}>
              Upload Paper
            </Button>
          </StyledPaper>
        </Grid>
      </Grid>

      <Typography variant="body2" align="center" sx={{ mt: 4, color: "#b0b0b0" }}>
        Loved by 600,000+ happy users worldwide
      </Typography>
    </Box>
  );
};

export default Home;
