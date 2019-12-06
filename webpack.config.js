const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const TerserPlugin = require('terser-webpack-plugin')
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  //mode: 'production',
  mode: 'none',
  context: __dirname,

  entry: {
    'ncrcrd': './assets/ncrcrd/js/index',
  },

  output: {
    path: path.resolve('./build/assets/'),
    filename: '[name]/js/app-[hash].js',
  },

  resolve: {
    alias: {vue: 'vue/dist/vue.js'},
  },

  optimization: {
    minimizer: [
      new TerserPlugin({
        cache: true,
        parallel: true,
        sourceMap: false,
      }),
      new OptimizeCSSAssetsPlugin({}),
    ],
  },

  plugins: [
    new BundleTracker({filename: './build/webpack-stats.json'}),
    new MiniCssExtractPlugin({
      filename: "[name]/css/app-[hash].css",
      chunkFilename: "[id]-[hash].css",
    }),
    new CopyWebpackPlugin([
      { from: './assets/ncrcrd/img/', to: 'ncrcrd/img/', toType: 'dir' },
      { from: './node_modules/open-iconic/font/fonts/', to: 'ncrcrd/fonts/', toType: 'dir' },
    ]),
    new VueLoaderPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
            options: { url: false },
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: function () {
                return [
                  require('precss'),
                  require('autoprefixer')
                ]
              },
            },
          },
          {
            loader: 'sass-loader',
          },
        ],
      },
    ],
  },
};
