import Vue from 'vue'
import '../css/index.scss'
import 'bootstrap'
import clamp from 'clamp-js-main'

import TableCorporation from './components/TableCorporation.vue'
import TableGuide from './components/TableGuide.vue'

window.modules = {
  Vue,
  clamp,

  app: new Vue({
    el: '#app',
    components: {
      TableCorporation,
      TableGuide,
    },
    data () {
      return {
        windowHeight: 0,
      }
    },
    watch: {
      windowHeight: function (newHeight) {
        // header:210px, body.margin-top:20px, body.margin-bottom:20px, footer:150px, total:400px
        let bodyMinHeight = newHeight - 400
        bodyMinHeight = bodyMinHeight > 0 ? bodyMinHeight : 0
        document.getElementById('body').style.minHeight = bodyMinHeight + 'px'
      },
    },
    mounted () {
      this.windowHeight = window.innerHeight
      this.$nextTick(() => {
        window.addEventListener('resize', () => {
          this.windowHeight = window.innerHeight
        })
      })
    },
  }),
}
