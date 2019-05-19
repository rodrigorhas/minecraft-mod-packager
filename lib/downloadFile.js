const request = require('request')
const fs = require('fs')

const download = function(url, dest) {
  return new Promise((resolve, reject) => {
    request.get(url, { encoding: null }, function(e, _r, b) {
      if (e) throw e;
      fs.writeFileSync(dest, b);
    });
  })
}

module.exports = download
