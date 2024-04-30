module.exports = {
    preset: '@vue/cli-plugin-unit-jest',  // Use the preset for Vue 3
    moduleFileExtensions: [
      'js',
      'json',
      // tell Jest to handle `*.vue` files
      'vue'
    ],
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1'
    },
    transformIgnorePatterns: [
      '/node_modules/(?!axios).+\\.js$'
    ],
    transform: {
      // process `*.vue` files with `vue-jest`
      '^.+\\.vue$': '@vue/vue3-jest',  // Use Vue 3 compatible jest transformer
      '^.+\\.js$': 'babel-jest',  // Ensure Babel processes JS files
    }
  };
  
