import { Box, Heading, Button } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <Box textAlign="center" mt="20">
      <Heading as="h1" size="xl" mb="8">
        Welcome to Spotify Shopper
      </Heading>
      <Button onClick={handleLogin} colorScheme="teal" size="lg">
        Login with Spotify
      </Button>
    </Box>
  );
};

export default Landing;
