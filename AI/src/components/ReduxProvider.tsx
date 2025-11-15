import { ReactNode } from 'react';
import { Provider } from 'react-redux';
import { store } from '../store';
import ErrorBoundary from './ErrorBoundary';

interface ReduxProviderProps {
  children: ReactNode;
}

const ReduxProvider = ({ children }: ReduxProviderProps) => {
  return (
    <ErrorBoundary>
      <Provider store={store}>
        {children}
      </Provider>
    </ErrorBoundary>
  );
};

export default ReduxProvider;
