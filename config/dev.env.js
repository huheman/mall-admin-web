'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // BASE_API: '"http://localhost:8201/mall-admin"' // 本地
  BASE_API: '"https://www.huhp.cc/api/mall-admin"' // 测试
})
