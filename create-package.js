const downloadFile = require('./lib/downloadFile')
const relations = require('./output/forge-mod-relations.json')
const path = require('path')
const fs = require('fs-extra')

async function init () {
  const version = '1.12.2'
  const modlist = relations.find(relation => relation.version === version)

  const mineForge = require('./output/minecraft-versions.json').find(mf => mf.version === version)

  if (!modlist || !mineForge) {
    return console.log(`Error, version ${version} isn't valid`)
  }

  const packageFolder = path.resolve(__dirname, `./output/modpack-${version}/`)
  fs.mkdirp(packageFolder)
  fs.mkdirp(packageFolder + '/mods/')
  
  const modsDownloadList = modlist.mods.slice(3).map((mod) => {
    const fileUrl = mod.file.url
    const url = `https://minecraft.curseforge.com${fileUrl}`
    const normalizedName = mod.file.filename.endsWith('.jar') ? mod.file.filename : mod.file.filename + '.jar'

    console.log(`download mod ${normalizedName}\nfrom url: ${url}\n`)

    return downloadFile(
      url,
      path.join(packageFolder, '/mods/', normalizedName)
    )
  })

  const downloadForge = async (forge, type) => {
    const {name, url} = forge[type]

    console.log(`download mod ${type}-${name}\nfrom url: ${url}\n`)

    return downloadFile(
      url,
      path.join(packageFolder, `${type}-${name}`)
    )
  }

  modsDownloadList.concat([
    downloadForge(mineForge, 'server'),
    downloadForge(mineForge, 'client')
  ])

  Promise.all(modsDownloadList)
    .then(() => {
      console.log('all done')
    })
    .catch((error) => {
      console.log('something goes wrong', error)
    })
}

init()