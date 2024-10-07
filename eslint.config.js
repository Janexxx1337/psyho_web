import prettierPlugin from 'eslint-plugin-prettier';
import vuePlugin from 'eslint-plugin-vue';

export default [
	{
		files: ['src/**/*.vue', 'src/**/*.js', 'src/**/*.ts'],
		languageOptions: {
			ecmaVersion: 2021,
			sourceType: 'module',
		},
		plugins: {
			vue: vuePlugin,
			prettier: prettierPlugin,
		},
		rules: {
			// Prettier
			'prettier/prettier': 'error',

			// Vue-specific rules
			'vue/multi-word-component-names': 'off',

			// JS/TS rules
			'no-unused-vars': ['error', { vars: 'all', args: 'none' }],
		},
	},
];
