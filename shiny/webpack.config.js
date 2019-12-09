const path = require("path");

module.exports = {
    output: {
      path: path.resolve(__dirname, 'www'),
      filename: 'main.js'
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: 'babel-loader',
                exclude: /node_modules/
            }
        ]
    },
    mode: "production"
  };