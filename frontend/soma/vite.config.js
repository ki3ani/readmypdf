import reactRefresh from '@vitejs/plugin-react';

export default {
  plugins: [reactRefresh()],
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
    },
  },
};
