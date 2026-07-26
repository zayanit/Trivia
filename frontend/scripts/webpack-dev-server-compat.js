const configPath = require.resolve(
  "react-scripts/config/webpackDevServer.config"
);
const createDevServerConfig = require(configPath);
const WebpackDevServer = require("webpack-dev-server");

WebpackDevServer.prototype.close = WebpackDevServer.prototype.stopCallback;

require.cache[configPath].exports = (...args) => {
  const {
    https,
    onBeforeSetupMiddleware,
    onAfterSetupMiddleware,
    ...config
  } = createDevServerConfig(...args);

  return {
    ...config,
    ...(https && {
      server: typeof https === "object" ? { type: "https", options: https } : "https",
    }),
    setupMiddlewares(middlewares, devServer) {
      onBeforeSetupMiddleware(devServer);

      const afterMiddlewares = [];
      const use = devServer.app.use;
      devServer.app.use = middleware => {
        afterMiddlewares.push(middleware);
        return devServer.app;
      };

      try {
        onAfterSetupMiddleware(devServer);
      } finally {
        devServer.app.use = use;
      }

      return [...middlewares, ...afterMiddlewares];
    },
  };
};
