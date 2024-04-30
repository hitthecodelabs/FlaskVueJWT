module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
        logLevel: 'debug'  // This will enable verbose logging for the proxy
      },
    },
  },
};
