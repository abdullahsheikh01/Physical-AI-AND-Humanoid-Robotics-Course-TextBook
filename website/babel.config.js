module.exports = {
  presets: [require.resolve('@docusaurus/core/lib/babel/preset')],
  plugins: [
    // CSS Modules support
    [
      'module-resolver',
      {
        alias: {
          '@site': './',
          '@components': './src/components',
          '@css': './src/css',
        },
      },
    ],
  ],
};