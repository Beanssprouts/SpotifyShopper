import { useState } from 'react';
import { Box, Heading, Input, Button, Flex } from '@chakra-ui/react';

const Home = () => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    // Implement search functionality here
  };

  return (
    <Box textAlign="center" mt="20">
      <Heading as="h1" size="xl" mb="8">
        Welcome to Spotify Shopper
      </Heading>
      <Flex justify="center" mb="4">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for tracks"
          size="lg"
          width="400px"
          mr="4"
        />
        <Button onClick={handleSearch} colorScheme="teal" size="lg">
          Search
        </Button>
      </Flex>
    </Box>
  );
};

export default Home;
