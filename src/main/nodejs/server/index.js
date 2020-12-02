const consola = require('consola')
const { Nuxt, Builder } = require('nuxt')
const config = require('../nuxt.config.js')
const app = require('./app')

// Import and Set Nuxt.js options
config.dev = (process.env.NODE_ENV !== 'production')

async function start () {
  // Init Nuxt.js
  const nuxt = new Nuxt(config)
  await nuxt.ready()

  const {
    host = process.env.HOST || '0.0.0.0',
    port = process.env.PORT || 3000
  } = nuxt.options.server

  // Build only in dev mode
  if (config.dev) {
    const builder = new Builder(nuxt)
    await builder.build()
  }

  // Give nuxt middleware to express
  app.use(nuxt.render)

  // Listen the server
  app.listen(port, host)
  consola.ready({
    message: `Server listening on http://${host}:${port}; 
      BASE = ${process.BASE || process.env.BASE || process.env.npm_package_config_base || '' }
      `,
      // ${JSON.stringify(process.env, null, 4)}
      // `
     badge: true
  })
}

start()
