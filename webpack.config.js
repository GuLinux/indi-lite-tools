var path = require('path');
var webpack = require('webpack');

module.exports = {
    output: {
        path: __dirname,
        filename: 'bundle.js',
        publicPath: '/static/'
    },
    module: {
        loaders: [
            {
                test: /.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: ['es2015', 'react']
                }
            },
            {
                test   : /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
                loader : 'file-loader'
            },
            {
                    test: /\.css$/, 
                    loader: "style-loader!css-loader"
            }
        ]
    },
};
