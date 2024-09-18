import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';
import Landing from './components/Landing';
import { ChakraProvider } from '@chakra-ui/react';
import { useSpotify } from './context/SpotifyContext';

const App: React.FC = () => {
  const { state } = useSpotify();

  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={state.token ? <Navigate to="/home" /> : <Landing />} />
          <Route path="/login" element={state.token ? <Navigate to="/home" /> : <Login />} />
          <Route path="/home" element={state.token ? <Home /> : <Navigate to="/" />} />
          {/* Other routes will be added here later */}
        </Routes>
      </Router>
    </ChakraProvider>
  );
};

export default App;
