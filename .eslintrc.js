module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    'plugin:prettier/recommended',
  ],
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module',
  },
  rules: {
    'vue/multi-word-component-names': 0,
    'prettier/prettier': 'error',
    'no-unused-vars': ['error', { 'vars': 'all', 'args': 'none' }],
  },
};
