const fs = require('fs')
const promisify = require('util').promisify;

const $writeFile = promisify(fs.writeFile);

function setConcat(...iterables) {
  const set = new Set();

  for (let iterable of iterables) {
    for (let item of iterable) {
      set.add(item);
    }
  }

  return set;
}

function getUniqueModVersions (data) {
  let availableVersions = new Set()

  data.forEach((mod) => {
    const modUniqueVersions = new Set(mod.versions.map((file) => file.version));
    availableVersions = setConcat(availableVersions, modUniqueVersions)
  })

  return availableVersions;
}

async function createRelations () {
  const data = require('./mods/data.json')

  const uniqueModVersions = getUniqueModVersions(data)

  const uniqueModFilesPerVersion = Array.from(uniqueModVersions.keys()).reduce((versionList, version) => {
    const modsPerVersion = data.reduce((acc, mod) => {
      const modFile = mod.versions.find(file => file.version === version)
      if (modFile) {
        acc.push({
          mod: mod.name,
          file: modFile
        })
      }

      return acc;
    }, [])

    versionList.push({
      version,
      mods: modsPerVersion,
      count: modsPerVersion.length
    })

    return versionList
  }, []).sort((a, b) => b.count - a.count)

  uniqueModFilesPerVersion.slice(0, 5).forEach((x) => {
    console.log({
      version: x.version,
      count: x.count
    })
  })

  try {
    $writeFile('./output/forge-mod-relations.json', JSON.stringify(uniqueModFilesPerVersion.slice(0, 5)))
    console.log('related-data.json writed')
  } catch (error) {
    console.log(error)
  }
}

createRelations()
