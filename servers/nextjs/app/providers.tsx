'use client';

import { Provider } from 'react-redux';
import { store } from '../store/store';

export function Providers({ children }: { children: React.ReactNode }) {
<<<<<<< HEAD
  return <Provider store={store}>
      {children}
  </Provider>;
=======
  return <Provider store={store}>{children}</Provider>;
>>>>>>> 78e1006 (Initial: presenton)
}
