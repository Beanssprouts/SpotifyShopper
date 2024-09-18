import React from 'react';
import { Button, Box, Heading } from '@chakra-ui/react';
import { useSpotify } from '../context/SpotifyContext';
import { login } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const { dispatch } = useSpotify();
  const navigate = useNavigate();

  const handleLogin = () => {
    const clientId = import.meta.env.VITE_SPOTIFY_CLIENT_ID;
    const redirectUri = import.meta.env.VITE_SPOTIFY_REDIRECT_URI;
    const scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private';
    const authUrl = `https://accounts.spotify.com/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
    window.location.href = authUrl;
  };

  React.useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    if (code) {
      login(code)
        .then((response) => {
          dispatch({ type: 'SET_TOKEN', payload: response.data.token });
          dispatch({ type: 'SET_USER', payload: response.data.user });
          navigate('/home');
        })
        .catch((error) => {
          console.error('Error during login:', error);
        });
    }
  }, [dispatch, navigate]);

  return (
    <Box textAlign="center" mt="20">
      <Heading as="h1" size="xl" mb="8">
        Login to Spotify Shopper
      </Heading>
      <Button onClick={handleLogin} colorScheme="teal" size="lg">
        Login with Spotify
      </Button>
    </Box>
  );
};

export default Login;
