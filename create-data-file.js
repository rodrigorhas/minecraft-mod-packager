const fs = require('fs')
const promisify = require('util').promisify;

const $readdir = promisify(fs.readdir);
const $writeFile = promisify(fs.writeFile);

async function createDataFile () {
  let allFiles = []
  const files = await $readdir('mods')

  for (fileName of files) {
    if (fileName !== 'data.json') {
      const file = require(`./mods/${fileName}`)
      allFiles = allFiles.concat({
        name: fileName.replace('.json', ''),
        versions: file
      })
    }
  }

  try {
    $writeFile('./mods/data.json', JSON.stringify(allFiles))
    console.log('data.json writed')
  } catch (error) {
    console.log(error)
  }
}

createDataFile()