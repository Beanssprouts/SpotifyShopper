import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const login = (code: string) =>
  api.post('/accounts/spotify-callback/', { code })
    .then((response) => response.data);

export const getUserData = (token: string) =>
  api.get('/accounts/user/', {
    headers: { Authorization: `Bearer ${token}` },
  });

export const searchSongs = (query: string, token: string) =>
  api.get('/playlists/search/', {
    params: { query },
    headers: { Authorization: `Bearer ${token}` },
  });

export const addToCart = (song: any, token: string) =>
  api.post('/cart-items/', song, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const createPlaylist = (name: string, token: string) =>
  api.post('/playlists/create-playlist/', { name }, {
    headers: { Authorization: `Bearer ${token}` },
  });
