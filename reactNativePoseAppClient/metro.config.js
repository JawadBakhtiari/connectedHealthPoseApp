const { getDefaultConfig, mergeConfig } = require("@react-native/metro-config");

const defaultConfig = getDefaultConfig(__dirname);
const { resolver: { sourceExts, assetExts } } = defaultConfig;

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 *
 * @type {import('metro-config').MetroConfig}
 */
const config = {
  resolver: {
    assetExts: [...assetExts, 'tflite'],
    sourceExts: [...sourceExts, 'js', 'json', 'ts', 'tsx'],
    resolverMainFields: ["sbmodern", "react-native", "browser", "main"],
  },
};

module.exports = mergeConfig(defaultConfig, config);
