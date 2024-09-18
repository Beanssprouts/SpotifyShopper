import React, { createContext, useReducer, useContext, ReactNode } from 'react';

interface State {
  user: any;
  cart: any[];
  token: string | null;
}

interface Action {
  type: string;
  payload?: any;
}

const initialState: State = {
  user: null,
  cart: [],
  token: null,
};

const SpotifyContext = createContext<{ state: State; dispatch: React.Dispatch<Action> }>({
  state: initialState,
  dispatch: () => undefined,
});

const spotifyReducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_TOKEN':
      return { ...state, token: action.payload };
    case 'ADD_TO_CART':
      return { ...state, cart: [...state.cart, action.payload] };
    case 'REMOVE_FROM_CART':
      return {
        ...state,
        cart: state.cart.filter((item) => item.id !== action.payload.id),
      };
    default:
      return state;
  }
};

export const SpotifyProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(spotifyReducer, initialState);
  return (
    <SpotifyContext.Provider value={{ state, dispatch }}>
      {children}
    </SpotifyContext.Provider>
  );
};

export const useSpotify = () => useContext(SpotifyContext);
