module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs'
  ],
  // add your custom rules here
  rules: {
      "vue/html-indent": 0, //"off"
      "vue/valid-v-for": 0, // Fix v-for/template/key bug
      "vue/no-v-html": 0,
      "vue/require-v-for-key": 0,
      "vue/html-self-closing": 0, // Disallow self-closing on HTML void elements (<input/>)
      "vue/require-prop-types": 0, // Prop "value" should define at least its type
      "vue/singleline-html-element-content-newline": 0,
      "vue/html-closing-bracket-spacing": 0,
      "vue/multiline-html-element-content-newline": 0,
      
      "unicorn/escape-case": 0,

      "indent": 0, //"off"
      "space-before-block": 0,
      "semi": 0,
      "comma-dangle": 0,
      "space-before-blocks": 0,
      "comma-spacing": 0,
      "quotes": 0,
      "key-spacing": 0,
      "spaced-comment": 0,
      "no-multi-spaces": 0,
      "no-trainling-spaces": 0,
      "no-console": 0,
      "object-curly-spacing": 0,
      "space-in-parens": 0,
      "standard/object-curly-even-spacing": 0,
      "arrow-parens": 0,
      "space-infix-ops": 0,
      "no-trailing-spaces": 0,
      "camelcase": 0,
      "quote-props": 0,
      "array-bracket-spacing": 0,
      "computed-property-spacing": 0,
      "template-curly-spacing" : "off"



  }
}
