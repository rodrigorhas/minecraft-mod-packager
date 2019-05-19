const fs = require('fs')
const path = require('path')
const promisify = require('util').promisify;

const $readdir = promisify(fs.readdir);
const $writeFile = promisify(fs.writeFile);

async function changeKey () {
  const abspath = path.resolve(__dirname, '../mods/')
  const files = await $readdir('mods/')

  for (const filename of files) {
    if (filename !== 'data.json') {
      let mods = require(`../mods/${filename}`)
      mods = mods.map((mod) => {
        mod.url = mod.url + '/download'
        return mod
      })

      try {
        $writeFile(path.resolve(abspath, filename), JSON.stringify(mods))
        console.log(`${filename} rewrited`)
      } catch (error) {
        console.log(error)
      }
    }
  }
}

changeKey()