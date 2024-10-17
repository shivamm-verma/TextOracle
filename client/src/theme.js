import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#74f0ed', // Light cyan
    },
    secondary: {
      main: '#ea445a', // Soft pink
    },
    background: {
      default: '#000000', // Black background
      paper: '#1e1e1e', // Darker paper background for contrast
    },
    text: {
      primary: '#ffffff', // White text for readability
      secondary: '#b0b0b0', // Light gray for secondary text
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          transition: 'background-color 0.3s ease, transform 0.3s ease',
          '&:hover': {
            backgroundColor: '#ea445a', // Soft pink on hover
            transform: 'scale(1.05)', // Slight scale on hover
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          transition: 'background-color 0.3s ease, transform 0.3s ease',
          borderRadius: '12px',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.5)', // Soft shadow
          '&:hover': {
            transform: 'translateY(-2px)', // Lift effect on hover
          },
        },
      },
    },
  },
});

export default theme;
